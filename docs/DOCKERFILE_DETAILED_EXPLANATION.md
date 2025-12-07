# Dockerfile 详细解析

## 完整的构建和运行流程

### 构建时发生了什么

```bash
$ docker build -t fe-demo .
```

#### 阶段 1: Builder (构建阶段)

```
步骤 1: FROM node:18-alpine as builder
┌─────────────────────────────────────┐
│ 拉取 node:18-alpine 基础镜像        │
│ 大小: ~170MB                        │
│ 包含: Node.js 18, npm, Alpine Linux │
└─────────────────────────────────────┘

步骤 2: WORKDIR /app
┌─────────────────────────────────────┐
│ 在容器内创建并进入 /app 目录         │
│ 当前目录: /app                       │
└─────────────────────────────────────┘

步骤 3: COPY package*.json ./
┌─────────────────────────────────────┐
│ 复制:                                │
│   宿主机: ./package.json             │
│         → 容器: /app/package.json    │
│   宿主机: ./package-lock.json        │
│         → 容器: /app/package-lock.json│
│                                      │
│ 💡 缓存层: 只有这些文件变化才重建    │
└─────────────────────────────────────┘

步骤 4: RUN npm ci
┌─────────────────────────────────────┐
│ 执行: npm ci                         │
│                                      │
│ 过程:                                │
│ 1. 删除 node_modules/ (如果存在)    │
│ 2. 根据 package-lock.json 安装依赖  │
│ 3. 验证版本匹配                      │
│                                      │
│ 结果: /app/node_modules/             │
│       (约 200-500MB)                 │
│                                      │
│ ⏱️ 耗时: 30-120 秒                   │
│ 💡 缓存层: package.json 不变则使用缓存│
└─────────────────────────────────────┘

步骤 5: COPY . .
┌─────────────────────────────────────┐
│ 复制所有源代码:                      │
│                                      │
│ /app/                                │
│ ├── src/                   ✓         │
│ ├── index.html             ✓         │
│ ├── vite.config.ts         ✓         │
│ ├── tsconfig.json          ✓         │
│ ├── tailwind.config.ts     ✓         │
│ ├── node_modules/          (已存在)  │
│ ├── package.json           (已存在)  │
│ └── ...                              │
│                                      │
│ 忽略 (.dockerignore):                │
│ ├── .git/                  ✗         │
│ ├── dist/                  ✗         │
│ ├── .DS_Store              ✗         │
│ └── ...                              │
└─────────────────────────────────────┘

步骤 6: RUN npm run build
┌─────────────────────────────────────┐
│ 执行: tsc && vite build              │
│                                      │
│ TypeScript 编译:                     │
│   src/**/*.tsx → JavaScript          │
│   类型检查 ✓                         │
│                                      │
│ Vite 构建:                           │
│   - 打包所有模块                     │
│   - Tree shaking (移除未使用代码)   │
│   - 代码压缩                         │
│   - 资源优化                         │
│   - 生成 source maps                │
│                                      │
│ 输出: /app/dist/                     │
│ ├── index.html                       │
│ ├── assets/                          │
│ │   ├── index-[hash].js    (约 150KB)│
│ │   └── index-[hash].css   (约 20KB) │
│ └── apple-touch-icon.svg             │
│                                      │
│ ⏱️ 耗时: 10-30 秒                    │
└─────────────────────────────────────┘

此时 builder 阶段的文件系统:
/app/
├── node_modules/      (~300MB)  ← 不需要
├── src/              (~1MB)     ← 不需要
├── dist/             (~200KB)   ← 需要!
├── package.json                 ← 不需要
└── ...                          ← 不需要
```

#### 阶段 2: Nginx (运行阶段)

```
步骤 7: FROM nginx:alpine
┌─────────────────────────────────────┐
│ 🗑️  丢弃 builder 阶段的所有内容      │
│                                      │
│ 拉取全新的 nginx:alpine 镜像         │
│ 大小: ~23MB                          │
│ 包含: Nginx, Alpine Linux            │
│ 没有: Node.js, npm, 源代码           │
└─────────────────────────────────────┘

步骤 8: COPY nginx.conf /etc/nginx/conf.d/default.conf
┌─────────────────────────────────────┐
│ 复制自定义 Nginx 配置:               │
│                                      │
│ 宿主机: ./nginx.conf                 │
│      → /etc/nginx/conf.d/default.conf│
│                                      │
│ 配置内容:                            │
│ - 监听 80 端口                       │
│ - 根目录: /usr/share/nginx/html      │
│ - SPA 路由支持 (try_files)          │
│ - Gzip 压缩                          │
│ - 静态资源缓存                       │
│ - 健康检查端点 /health               │
└─────────────────────────────────────┘

步骤 9: COPY --from=builder /app/dist /usr/share/nginx/html
┌─────────────────────────────────────┐
│ 从 builder 阶段复制构建产物:         │
│                                      │
│ builder:/app/dist/                   │
│           ↓                          │
│ nginx:/usr/share/nginx/html/         │
│                                      │
│ 复制内容:                            │
│ /usr/share/nginx/html/               │
│ ├── index.html                       │
│ ├── assets/                          │
│ │   ├── index-abc123.js              │
│ │   └── index-def456.css             │
│ └── apple-touch-icon.svg             │
│                                      │
│ 💾 大小: ~200KB                      │
└─────────────────────────────────────┘

步骤 10: EXPOSE 80
┌─────────────────────────────────────┐
│ 文档化声明:                          │
│ 此容器将在 80 端口提供服务           │
│                                      │
│ 注意: 不会实际开放端口               │
└─────────────────────────────────────┘

步骤 11: CMD ["nginx", "-g", "daemon off;"]
┌─────────────────────────────────────┐
│ 设置容器启动命令:                    │
│                                      │
│ 运行: nginx -g "daemon off;"         │
│                                      │
│ Nginx 将:                            │
│ - 在前台运行 (不后台化)              │
│ - 监听 80 端口                       │
│ - 提供 /usr/share/nginx/html/ 的文件 │
│ - 应用自定义配置                     │
└─────────────────────────────────────┘

最终镜像构成:
┌─────────────────────────────────────┐
│ 总大小: ~23.5MB                      │
├─────────────────────────────────────┤
│ - Nginx                    (~23MB)   │
│ - 自定义配置               (~1KB)    │
│ - 静态文件 (dist/)         (~200KB)  │
└─────────────────────────────────────┘

✅ 构建完成!
```

### 运行时发生了什么

```bash
$ docker run -d -p 8080:80 fe-demo
```

```
容器启动流程:

1. 创建容器
┌─────────────────────────────────────┐
│ Docker 创建容器实例                  │
│ - 分配文件系统                       │
│ - 设置网络                           │
│ - 配置端口映射: 8080:80              │
└─────────────────────────────────────┘

2. 执行 CMD 指令
┌─────────────────────────────────────┐
│ 运行: nginx -g "daemon off;"         │
│                                      │
│ Nginx 启动:                          │
│ 1. 读取配置文件                      │
│ 2. 绑定 80 端口                      │
│ 3. 启动 worker 进程                  │
│ 4. 前台运行，等待请求                │
└─────────────────────────────────────┘

3. 就绪状态
┌─────────────────────────────────────┐
│ ✅ 容器运行中                        │
│ ✅ Nginx 监听 80 端口                │
│ ✅ 准备接受 HTTP 请求                │
└─────────────────────────────────────┘
```

### 访问应用

```
用户请求流程:

浏览器                    Docker                  容器
  │                        │                      │
  │ GET localhost:8080     │                      │
  ├───────────────────────>│                      │
  │                        │                      │
  │                        │ 转发到容器 :80       │
  │                        ├─────────────────────>│
  │                        │                      │
  │                        │                      │ Nginx 处理请求
  │                        │                      │ 读取 /usr/share/nginx/html/index.html
  │                        │                      │
  │                        │  返回 index.html     │
  │                        │<─────────────────────┤
  │                        │                      │
  │ 返回 HTML              │                      │
  │<───────────────────────┤                      │
  │                        │                      │
  │ GET /assets/index.js   │                      │
  ├───────────────────────>│─────────────────────>│
  │                        │                      │
  │                        │  返回 JS 文件        │
  │<───────────────────────┤<─────────────────────┤
  │                        │                      │
```

## 层缓存机制详解

Docker 使用层缓存来加快构建速度:

### 首次构建

```
步骤                             状态        耗时
────────────────────────────────────────────────
FROM node:18-alpine            拉取镜像     10s
WORKDIR /app                   新建         0.1s
COPY package*.json ./          新建         0.1s
RUN npm ci                     新建 ⏱️      60s
COPY . .                       新建         1s
RUN npm run build              新建 ⏱️      20s
FROM nginx:alpine              拉取镜像     5s
COPY nginx.conf                新建         0.1s
COPY --from=builder            新建         0.1s
────────────────────────────────────────────────
总计:                                      96s
```

### 再次构建（仅修改源代码）

```
步骤                             状态        耗时
────────────────────────────────────────────────
FROM node:18-alpine            使用缓存     0s
WORKDIR /app                   使用缓存     0s
COPY package*.json ./          使用缓存     0s
RUN npm ci                     使用缓存 ✨   0s
COPY . .                       重新构建     1s
RUN npm run build              重新构建 ⏱️  20s
FROM nginx:alpine              使用缓存     0s
COPY nginx.conf                使用缓存     0s
COPY --from=builder            重新构建     0.1s
────────────────────────────────────────────────
总计:                                      21s
```

**加速 78%!** 🚀

### 缓存失效触发条件

```
修改的文件              失效的层                        影响
─────────────────────────────────────────────────────────────
src/App.tsx           COPY . . 及之后所有层           需要重新构建
                      (npm ci 层仍然缓存)

package.json          COPY package*.json 及之后所有层  需要重新安装依赖
                      (很慢!)

nginx.conf            只有 COPY nginx.conf 层          很快

Dockerfile            所有层                           全部重建
```

## 最佳实践总结

### ✅ 这个 Dockerfile 做对的事情

1. **多阶段构建**
   - 分离构建和运行环境
   - 镜像从 800MB 减少到 23MB

2. **使用 Alpine 镜像**
   - 最小化基础镜像大小
   - 减少攻击面

3. **优化层缓存**
   - 先复制 package.json，后复制源代码
   - 利用缓存加快构建速度

4. **使用 npm ci**
   - 可重现的依赖安装
   - 生产环境最佳实践

5. **前台运行 Nginx**
   - daemon off 确保容器不退出
   - 正确的容器运行方式

6. **自定义 Nginx 配置**
   - SPA 路由支持
   - Gzip 压缩
   - 静态资源缓存

### 🎯 理解每一行的关键

```dockerfile
# 为什么这样写              →  达到什么效果
─────────────────────────────────────────────────
FROM ... as builder         →  命名阶段，便于引用
COPY package*.json ./       →  优化缓存，先安装依赖
RUN npm ci                  →  可重现构建
COPY . .                    →  最后复制源代码
RUN npm run build           →  生成静态文件
FROM nginx:alpine           →  轻量级 Web 服务器
COPY --from=builder         →  只取构建产物
daemon off                  →  保持容器运行
```

## 调试技巧

### 查看构建过程

```bash
# 详细输出
docker build --progress=plain -t fe-demo .

# 不使用缓存
docker build --no-cache -t fe-demo .

# 构建到特定阶段
docker build --target builder -t fe-demo-builder .
```

### 进入容器调试

```bash
# 进入运行中的容器
docker exec -it <container_id> sh

# 查看文件
ls -la /usr/share/nginx/html/

# 查看 Nginx 配置
cat /etc/nginx/conf.d/default.conf

# 查看日志
docker logs <container_id>
```

### 检查镜像大小

```bash
# 查看镜像详情
docker images fe-demo

# 查看镜像历史（每层大小）
docker history fe-demo

# 分析镜像
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest fe-demo
```

## 常见问题

### Q: 为什么不直接用 Node.js 镜像提供静态文件？

**A:**
- Node.js 镜像太大（~900MB）
- Nginx 是专业的静态文件服务器，性能更好
- 多阶段构建后镜像只有 23MB

### Q: EXPOSE 80 有什么用？

**A:**
- 文档化作用，告诉用户容器使用哪个端口
- docker-compose 可以自动使用这个信息
- 实际开放端口仍需要 -p 参数

### Q: 能不能不用 daemon off？

**A:** 不能！
- Docker 需要前台进程保持运行
- 如果 Nginx 后台运行，容器会立即退出

### Q: 为什么不把 nginx.conf 放在镜像里？

**A:**
- nginx.conf 是配置文件，分开管理更灵活
- 可以在不重建镜像的情况下更新配置
- 遵循"配置与代码分离"原则

## 总结

这个 Dockerfile 展示了现代 Docker 最佳实践:

1. ✅ 多阶段构建 → 小体积
2. ✅ 层缓存优化 → 快构建
3. ✅ 生产级配置 → 高性能
4. ✅ 清晰的结构 → 易维护

每一行都有其存在的理由，理解这些原理可以帮助你编写更好的 Dockerfile！
