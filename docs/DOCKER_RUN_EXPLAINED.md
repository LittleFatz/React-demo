# Docker Run 命令详解

## 命令完整解析

```bash
docker run -d -p 8080:80 --name my-app fe-demo:latest
```

让我们逐个拆解每个部分：

## 📋 命令结构

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
    │         │        │        │        │
    │         │        │        │        └─ 传递给容器的参数
    │         │        │        └─ 容器启动后执行的命令
    │         │        └─ 使用的镜像
    │         └─ 各种选项/参数
    └─ Docker 运行命令
```

## 🔍 逐部分解析

### 1. `docker run`

**作用**: Docker 的核心命令，用于创建并启动一个新容器

**工作流程**:
```
docker run
    ↓
检查本地是否有镜像
    ↓
从镜像创建容器
    ↓
启动容器
    ↓
执行容器内的启动命令
```

**等价操作**:
```bash
# docker run 等于以下两步的组合:
docker create IMAGE  # 创建容器
docker start <容器ID>  # 启动容器
```

---

### 2. `-d` (detach)

**全称**: `--detach`

**作用**: 后台运行模式（守护进程模式）

**对比说明**:

#### 不加 `-d` (前台模式)
```bash
docker run fe-demo:latest

# 效果:
- 终端被占用 ❌
- 日志直接输出到终端
- Ctrl+C 会停止容器
- 终端关闭容器也停止
```

#### 加 `-d` (后台模式) ✅
```bash
docker run -d fe-demo:latest

# 效果:
- 返回容器ID后立即释放终端 ✅
- 容器在后台运行 ✅
- 可以继续执行其他命令 ✅
- 关闭终端容器仍然运行 ✅
```

**实际演示**:
```bash
# 前台运行
$ docker run fe-demo:latest
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/12/01 13:30:38 [notice] 1#1: nginx/1.29.3
(占用终端，需要 Ctrl+C 停止)

# 后台运行
$ docker run -d fe-demo:latest
9d5a2a3084b30402335f4e812132d4f606df70d7
(立即返回容器ID，终端可用)
$ █  (可以继续输入其他命令)
```

---

### 3. `-p 8080:80` (port mapping)

**全称**: `--publish 8080:80`

**作用**: 端口映射/端口转发

**格式**: `-p [宿主机端口]:[容器端口]`

**详细说明**:

```
┌─────────────────────────────────────────────────────┐
│                    你的电脑 (宿主机)                  │
│                                                      │
│  浏览器访问 localhost:8080                           │
│         │                                            │
│         ↓                                            │
│  ┌──────────────────────────────────┐               │
│  │    Docker Engine                 │               │
│  │                                  │               │
│  │  端口 8080 (宿主机)               │               │
│  │      ↓ 映射                      │               │
│  │  ┌─────────────────────────┐    │               │
│  │  │   容器 (Container)       │    │               │
│  │  │                         │    │               │
│  │  │   端口 80 (容器内)       │    │               │
│  │  │      ↓                  │    │               │
│  │  │   Nginx 监听 80 端口     │    │               │
│  │  │      ↓                  │    │               │
│  │  │   返回网页               │    │               │
│  │  └─────────────────────────┘    │               │
│  └──────────────────────────────────┘               │
└─────────────────────────────────────────────────────┘
```

**为什么需要端口映射?**

容器内部是隔离的网络环境:

```
没有端口映射:
  浏览器 → 容器的 80 端口 ❌ 无法访问（容器网络隔离）

有端口映射 -p 8080:80:
  浏览器 → 宿主机 8080 → 容器 80 ✅ 可以访问
```

**端口映射示例**:

```bash
# 映射到相同端口
-p 80:80              # 宿主机80 → 容器80
访问: http://localhost:80

# 映射到不同端口（常用）
-p 8080:80            # 宿主机8080 → 容器80
访问: http://localhost:8080

# 映射多个端口
-p 8080:80 -p 8443:443  # HTTP和HTTPS
访问: http://localhost:8080
     https://localhost:8443

# 只指定容器端口（宿主机随机分配）
-p 80                 # 宿主机随机端口 → 容器80

# 指定 IP
-p 127.0.0.1:8080:80  # 只允许本地访问

# 映射所有端口
-P                    # 自动映射所有 EXPOSE 的端口
```

**常见场景**:

```bash
# 场景1: 本地开发（避免冲突）
docker run -p 8080:80 app1  # 第一个应用
docker run -p 8081:80 app2  # 第二个应用
docker run -p 8082:80 app3  # 第三个应用

# 场景2: 标准端口
docker run -p 80:80 web     # HTTP
docker run -p 443:443 web   # HTTPS

# 场景3: 数据库
docker run -p 3306:3306 mysql      # MySQL
docker run -p 5432:5432 postgres   # PostgreSQL
docker run -p 6379:6379 redis      # Redis
```

---

### 4. `--name my-app`

**作用**: 给容器指定一个名称

**为什么需要名称?**

#### 不指定名称（Docker 自动生成）
```bash
docker run -d fe-demo:latest

# Docker 随机生成名称
docker ps
CONTAINER ID   NAME
abc123def456   angry_einstein      ← 随机生成
```

#### 指定名称 ✅
```bash
docker run -d --name my-app fe-demo:latest

# 使用你指定的名称
docker ps
CONTAINER ID   NAME
abc123def456   my-app              ← 你指定的名称
```

**名称的用途**:

```bash
# 使用容器ID（不方便）
docker stop abc123def456
docker logs abc123def456
docker exec -it abc123def456 sh

# 使用容器名称（方便）✅
docker stop my-app
docker logs my-app
docker exec -it my-app sh
```

**名称规则**:

```bash
# ✅ 有效名称
my-app
web-server
database_01
redis-cache

# ❌ 无效名称
my app           # 不能有空格
123-app          # 不能以数字开头
my_app!          # 不能有特殊字符（除了 - 和 _）
```

**名称必须唯一**:

```bash
# 第一次运行
docker run --name my-app fe-demo:latest  ✅

# 再次运行相同名称
docker run --name my-app fe-demo:latest  ❌
Error: The container name "/my-app" is already in use

# 解决方法：
# 1. 使用不同名称
docker run --name my-app-2 fe-demo:latest

# 2. 删除旧容器
docker rm my-app
docker run --name my-app fe-demo:latest
```

---

### 5. `fe-demo:latest`

**格式**: `[REPOSITORY]:[TAG]`

**作用**: 指定要使用的镜像

**详细说明**:

```
fe-demo:latest
   │      │
   │      └─ 标签(tag) - 版本标识
   └─ 仓库名(repository) - 镜像名称
```

**标签说明**:

```bash
# 指定标签
fe-demo:latest    # 最新版本
fe-demo:v1.0.0    # 特定版本
fe-demo:dev       # 开发版本
fe-demo:prod      # 生产版本

# 不指定标签（默认为 latest）
fe-demo           # 等同于 fe-demo:latest
```

**完整镜像名称格式**:

```
[REGISTRY/][NAMESPACE/]REPOSITORY[:TAG]

例如:
docker.io/library/nginx:alpine
    │       │       │     │
    │       │       │     └─ 标签
    │       │       └─ 仓库名
    │       └─ 命名空间
    └─ 镜像仓库地址

简写:
nginx:alpine      # Docker 自动补全为 docker.io/library/nginx:alpine
fe-demo:latest    # 本地镜像（没有仓库地址）
```

---

## 🎯 完整命令工作流程

```bash
docker run -d -p 8080:80 --name my-app fe-demo:latest
```

**执行步骤**:

```
1. Docker 检查本地是否有 fe-demo:latest 镜像
   ├─ 有 → 继续
   └─ 没有 → 尝试从 Docker Hub 拉取

2. 创建新容器
   ├─ 基于 fe-demo:latest 镜像
   ├─ 命名为 "my-app"
   └─ 配置端口映射 8080:80

3. 启动容器
   ├─ 后台运行 (-d)
   └─ 执行镜像中定义的启动命令 (CMD)

4. 配置网络
   └─ 将宿主机 8080 端口绑定到容器 80 端口

5. 返回容器 ID
   └─ 例如: 9d5a2a3084b30402335f4e812132d4f606df70d7

6. 容器运行中
   └─ 可以通过 http://localhost:8080 访问
```

## 📊 常用选项对比

### 基本运行模式

```bash
# 最简单（前台运行）
docker run fe-demo:latest
- 前台运行 ❌
- 无端口映射 ❌
- 随机名称 ❌

# 推荐方式（后台运行）
docker run -d -p 8080:80 --name my-app fe-demo:latest
- 后台运行 ✅
- 端口映射 ✅
- 自定义名称 ✅
```

### 其他常用选项

```bash
# 环境变量
docker run -d -p 8080:80 \
  -e NODE_ENV=production \
  -e API_KEY=abc123 \
  --name my-app fe-demo:latest

# 挂载卷（持久化数据）
docker run -d -p 8080:80 \
  -v /host/path:/container/path \
  --name my-app fe-demo:latest

# 内存限制
docker run -d -p 8080:80 \
  --memory="512m" \
  --cpus="1.0" \
  --name my-app fe-demo:latest

# 自动重启
docker run -d -p 8080:80 \
  --restart=unless-stopped \
  --name my-app fe-demo:latest

# 网络设置
docker run -d -p 8080:80 \
  --network=my-network \
  --name my-app fe-demo:latest

# 交互式运行（用于调试）
docker run -it --rm fe-demo:latest sh
  -i  交互模式
  -t  分配伪终端
  --rm 退出后自动删除容器
  sh  执行 shell

# 只读文件系统（安全）
docker run -d -p 8080:80 \
  --read-only \
  --name my-app fe-demo:latest

# 健康检查
docker run -d -p 8080:80 \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --name my-app fe-demo:latest
```

## 🔄 完整使用示例

### 示例 1: 标准 Web 应用

```bash
# 运行容器
docker run -d \
  -p 8080:80 \
  --name my-web-app \
  --restart=unless-stopped \
  fe-demo:latest

# 验证
docker ps | grep my-web-app

# 访问
curl http://localhost:8080

# 查看日志
docker logs my-web-app

# 停止
docker stop my-web-app

# 删除
docker rm my-web-app
```

### 示例 2: 开发环境

```bash
# 运行容器（挂载代码目录）
docker run -d \
  -p 8080:80 \
  -v $(pwd)/dist:/usr/share/nginx/html \
  --name dev-server \
  fe-demo:latest

# 修改代码后自动更新（因为挂载了目录）
```

### 示例 3: 多实例运行

```bash
# 运行多个实例
docker run -d -p 8080:80 --name app-1 fe-demo:latest
docker run -d -p 8081:80 --name app-2 fe-demo:latest
docker run -d -p 8082:80 --name app-3 fe-demo:latest

# 访问不同实例
curl http://localhost:8080  # app-1
curl http://localhost:8081  # app-2
curl http://localhost:8082  # app-3
```

## ⚠️ 常见错误和解决方法

### 错误 1: 端口被占用

```bash
docker run -d -p 8080:80 --name my-app fe-demo:latest

Error: Bind for 0.0.0.0:8080 failed: port is already allocated
```

**原因**: 端口 8080 已被占用

**解决**:
```bash
# 方法1: 使用其他端口
docker run -d -p 8081:80 --name my-app fe-demo:latest

# 方法2: 查找并停止占用端口的进程
lsof -i :8080
kill <PID>

# 方法3: 停止占用端口的容器
docker ps | grep 8080
docker stop <容器名>
```

### 错误 2: 容器名称冲突

```bash
docker run -d -p 8080:80 --name my-app fe-demo:latest

Error: The container name "/my-app" is already in use
```

**解决**:
```bash
# 方法1: 使用不同名称
docker run -d -p 8080:80 --name my-app-2 fe-demo:latest

# 方法2: 删除旧容器
docker rm my-app
docker run -d -p 8080:80 --name my-app fe-demo:latest

# 方法3: 不指定名称（自动生成）
docker run -d -p 8080:80 fe-demo:latest
```

### 错误 3: 镜像不存在

```bash
docker run -d -p 8080:80 my-typo:latest

Unable to find image 'my-typo:latest' locally
Error: pull access denied, repository does not exist
```

**解决**:
```bash
# 检查可用镜像
docker images

# 使用正确的镜像名称
docker run -d -p 8080:80 fe-demo:latest
```

### 错误 4: 容器立即退出

```bash
docker run -d --name my-app fe-demo:latest
# 容器启动后立即退出

docker ps -a
CONTAINER ID   STATUS
abc123def456   Exited (0) 2 seconds ago
```

**原因**: 容器内的主进程退出了

**解决**:
```bash
# 查看日志
docker logs my-app

# 常见原因：
# 1. 没有使用 daemon off（Nginx）
# 2. CMD 命令错误
# 3. 应用启动失败
```

## 📝 快速参考

### 常用命令模板

```bash
# 基础运行
docker run -d -p [宿主机端口]:80 --name [容器名] [镜像名]

# 带环境变量
docker run -d -p [端口]:80 -e KEY=value --name [名称] [镜像]

# 带数据卷
docker run -d -p [端口]:80 -v [宿主机路径]:[容器路径] --name [名称] [镜像]

# 完整配置
docker run -d \
  -p [端口]:80 \
  --name [名称] \
  --restart=unless-stopped \
  --memory="512m" \
  --cpus="1.0" \
  -e KEY=value \
  -v [路径]:[路径] \
  [镜像]
```

### 运行后常用命令

```bash
docker ps                    # 查看运行中的容器
docker ps -a                 # 查看所有容器
docker logs [容器]           # 查看日志
docker logs -f [容器]        # 实时查看日志
docker exec -it [容器] sh    # 进入容器
docker stop [容器]           # 停止容器
docker start [容器]          # 启动容器
docker restart [容器]        # 重启容器
docker rm [容器]             # 删除容器
docker rm -f [容器]          # 强制删除
```

## 总结

```bash
docker run -d -p 8080:80 --name my-app fe-demo:latest
    │      │  │          │            │
    │      │  │          │            └─ 使用 fe-demo:latest 镜像
    │      │  │          └─ 容器名称为 my-app
    │      │  └─ 端口映射：宿主机8080 → 容器80
    │      └─ 后台运行
    └─ 创建并启动容器

结果：
- 创建名为 "my-app" 的容器 ✅
- 基于 fe-demo:latest 镜像 ✅
- 后台运行 ✅
- 通过 http://localhost:8080 访问 ✅
```

这是 Docker 中最常用的命令之一，理解每个参数的作用对于容器管理至关重要！
