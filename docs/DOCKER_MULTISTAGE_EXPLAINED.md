# Docker 多阶段构建详解

## 什么是多阶段构建？

多阶段构建允许在一个 Dockerfile 中使用多个 `FROM` 语句，每个 `FROM` 指令开始一个新的构建阶段。

## 为什么需要多阶段构建？

### 问题场景

对于前端项目：
1. **构建时**需要：Node.js、npm、TypeScript、Vite 等构建工具
2. **运行时**只需要：静态文件（HTML/CSS/JS）+ Web 服务器（Nginx）

如果使用单阶段构建，最终镜像会包含所有构建工具，导致镜像臃肿。

## 架构对比

### 单阶段构建（不推荐）

```
┌─────────────────────────────────────┐
│    最终镜像 (~500MB - 1GB)           │
├─────────────────────────────────────┤
│ ✓ Nginx                             │
│ ✓ 静态文件 (dist/)                   │
│ ✗ Node.js (~100MB)                  │
│ ✗ npm                               │
│ ✗ node_modules (~200MB+)            │
│ ✗ 源代码 (src/)                      │
│ ✗ TypeScript 编译器                  │
│ ✗ Vite 构建工具                      │
│ ✗ 所有开发依赖                        │
└─────────────────────────────────────┘
```

### 多阶段构建（推荐）

```
阶段 1: 构建阶段 (builder)
┌─────────────────────────────────────┐
│    Node.js 镜像 (~500MB)             │
├─────────────────────────────────────┤
│ ✓ Node.js                           │
│ ✓ npm                               │
│ ✓ 源代码                             │
│ ✓ node_modules                      │
│ ✓ 构建工具                           │
│                                     │
│ 执行: npm run build                 │
│ 输出: dist/ 目录                     │
└─────────────────────────────────────┘
           │
           │ 只复制 dist/ 目录
           ↓
阶段 2: 运行阶段 (最终镜像)
┌─────────────────────────────────────┐
│    最终镜像 (~20-30MB)               │
├─────────────────────────────────────┤
│ ✓ Nginx (~20MB)                     │
│ ✓ 静态文件 (dist/)                   │
│                                     │
│ 构建阶段的内容全部被丢弃 ✗            │
└─────────────────────────────────────┘
```

## 代码解析

### 我们的 Dockerfile

```dockerfile
# ============================================
# 阶段 1: 构建阶段
# ============================================
FROM node:18-alpine as builder  # 给这个阶段命名为 "builder"

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci  # 安装所有依赖（包括 devDependencies）

# 构建应用
COPY . .
RUN npm run build  # 生成 dist/ 目录

# 此时这个阶段有：
# - Node.js 运行时
# - node_modules/ (几百 MB)
# - src/ 源代码
# - dist/ 构建产物 ← 我们只需要这个！


# ============================================
# 阶段 2: 运行阶段（最终镜像）
# ============================================
FROM nginx:alpine  # 全新的镜像，从头开始

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 关键行：从 builder 阶段只复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html
#     ^^^^^^^^^^^^^^
#     从 builder 阶段复制，而不是从当前文件系统

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# 最终镜像只包含：
# - Nginx
# - dist/ 目录的静态文件
# - 没有 Node.js、npm、源代码等
```

## 关键语法说明

### `FROM ... as <name>`
```dockerfile
FROM node:18-alpine as builder
```
- 给这个构建阶段命名为 `builder`
- 后续阶段可以引用这个名字

### `COPY --from=<stage>`
```dockerfile
COPY --from=builder /app/dist /usr/share/nginx/html
```
- `--from=builder`: 从名为 `builder` 的阶段复制文件
- `/app/dist`: builder 阶段中的路径
- `/usr/share/nginx/html`: 当前阶段（最终镜像）的路径

## 优势总结

### 1. 镜像体积大幅减小
- **单阶段**: 500MB - 1GB
- **多阶段**: 20MB - 30MB
- **减少**: 95% 以上

### 2. 安全性提升
- 最终镜像不包含源代码
- 不包含开发工具和依赖
- 减少攻击面

### 3. 部署速度提升
- 镜像更小，拉取更快
- 容器启动更快
- 减少存储和带宽成本

### 4. 清晰的关注点分离
- 构建阶段：专注于编译和构建
- 运行阶段：专注于提供服务

## 镜像大小实测对比

### 单阶段构建
```bash
$ docker images
REPOSITORY          TAG          SIZE
fe-demo-single     latest       782MB
```

### 多阶段构建
```bash
$ docker images
REPOSITORY          TAG          SIZE
fe-demo-multi      latest       23.5MB
```

**节省空间**: 758.5MB (97% 减少)

## 常见应用场景

### 1. 前端项目（React/Vue/Angular）
```dockerfile
FROM node:18 as builder
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### 2. Go 项目
```dockerfile
FROM golang:1.21 as builder
RUN go build -o app

FROM alpine:latest
COPY --from=builder /app/app /app
```

### 3. Java 项目
```dockerfile
FROM maven:3-openjdk-17 as builder
RUN mvn clean package

FROM openjdk:17-slim
COPY --from=builder /app/target/*.jar app.jar
```

## 高级用法

### 多个构建阶段
```dockerfile
# 阶段 1: 依赖下载
FROM node:18 as deps
COPY package*.json ./
RUN npm ci

# 阶段 2: 构建
FROM node:18 as builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# 阶段 3: 测试
FROM node:18 as tester
COPY --from=builder /app .
RUN npm test

# 阶段 4: 生产镜像
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### 从外部镜像复制
```dockerfile
# 从官方镜像复制可执行文件
COPY --from=nginx:latest /usr/bin/nginx /usr/bin/nginx
```

## 最佳实践

1. **为阶段命名**: 使用有意义的名字（builder、tester、production）
2. **最小化最终镜像**: 只复制运行时需要的文件
3. **使用 alpine 镜像**: 减小基础镜像体积
4. **合理利用缓存**: 先复制 package.json，再复制源代码
5. **安全扫描**: 最终镜像更小，扫描更快更安全

## 调试技巧

### 查看某个阶段的镜像
```bash
# 构建到特定阶段
docker build --target builder -t fe-demo-builder .

# 进入该阶段查看
docker run -it fe-demo-builder sh
```

### 查看各阶段大小
```bash
docker build --target builder -t stage1 .
docker build -t stage2 .

docker images | grep stage
```

## 总结

多阶段构建是 Docker 的最佳实践之一，特别适合：
- ✅ 需要编译的项目（前端、Go、Java、C++ 等）
- ✅ 构建工具和运行环境不同的场景
- ✅ 需要优化镜像大小的场景
- ✅ 需要提高安全性的生产环境

对于前端项目来说，使用多阶段构建几乎是标配，能够将镜像大小从接近 1GB 减少到几十 MB，同时提高安全性和部署效率。
