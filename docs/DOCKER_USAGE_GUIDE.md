# Docker 镜像构建和使用指南

## 📦 镜像已经在你的本地了！

当你执行 `docker build` 命令后，镜像会**自动保存**在本地 Docker Desktop 中，不需要"推送"。

## 🎉 构建结果

```bash
✅ 镜像名称: fe-demo:latest
✅ 镜像大小: 53.6MB
✅ 构建时间: ~10秒（利用缓存后）
✅ 状态: 已保存在本地 Docker
```

## 🔍 查看本地镜像

### 方法 1: 命令行查看

```bash
# 查看所有镜像
docker images

# 只查看 fe-demo 镜像
docker images fe-demo

# 查看详细信息
docker inspect fe-demo:latest
```

### 方法 2: Docker Desktop GUI 查看

1. 打开 Docker Desktop 应用
2. 点击左侧 **Images** 标签
3. 找到 `fe-demo:latest` 镜像

你会看到：
- 镜像名称和标签
- 镜像大小
- 创建时间
- 可以直接点击运行

## 🚀 运行容器的多种方式

### 方式 1: 命令行运行

```bash
# 基本运行
docker run -d -p 8080:80 --name my-fe-demo fe-demo:latest

# 参数说明：
# -d              后台运行
# -p 8080:80      端口映射（宿主机:容器）
# --name          给容器命名
# fe-demo:latest  使用的镜像
```

**访问应用**: 浏览器打开 http://localhost:8080

### 方式 2: Docker Desktop GUI 运行

1. 在 Images 页面找到 `fe-demo:latest`
2. 点击右侧的 **Run** 按钮
3. 在弹出的设置中：
   - **Container name**: my-fe-demo
   - **Ports**: Host port `8080` → Container port `80`
4. 点击 **Run**

### 方式 3: 使用 docker-compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    image: fe-demo:latest
    container_name: fe-demo
    ports:
      - "8080:80"
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

## 🛠️ 常用命令

### 容器管理

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器日志
docker logs my-fe-demo

# 实时查看日志
docker logs -f my-fe-demo

# 停止容器
docker stop my-fe-demo

# 启动已停止的容器
docker start my-fe-demo

# 重启容器
docker restart my-fe-demo

# 删除容器
docker rm my-fe-demo

# 强制删除运行中的容器
docker rm -f my-fe-demo
```

### 镜像管理

```bash
# 查看镜像历史（每层大小）
docker history fe-demo:latest

# 查看镜像详细信息
docker inspect fe-demo:latest

# 给镜像打新标签
docker tag fe-demo:latest fe-demo:v1.0.0

# 删除镜像
docker rmi fe-demo:latest

# 清理未使用的镜像
docker image prune

# 清理所有未使用的资源
docker system prune -a
```

### 进入容器调试

```bash
# 进入运行中的容器
docker exec -it my-fe-demo sh

# 在容器内可以执行：
ls /usr/share/nginx/html/          # 查看静态文件
cat /etc/nginx/conf.d/default.conf # 查看 Nginx 配置
nginx -t                            # 测试 Nginx 配置
exit                                # 退出容器
```

## 🔄 重新构建镜像

### 修改代码后重新构建

```bash
# 重新构建（使用缓存，快）
docker build -t fe-demo:latest .

# 不使用缓存构建（慢，但干净）
docker build --no-cache -t fe-demo:latest .

# 构建并打新版本标签
docker build -t fe-demo:v2.0.0 .
```

### 构建优化技巧

```bash
# 查看构建过程详细信息
docker build --progress=plain -t fe-demo:latest .

# 只构建到特定阶段（调试用）
docker build --target builder -t fe-demo-builder .
```

## 📤 推送到远程镜像仓库

如果你想把镜像分享给其他人或部署到远程服务器，需要推送到镜像仓库。

### 推送到 Docker Hub

```bash
# 1. 登录 Docker Hub
docker login

# 2. 给镜像打标签（需要包含你的 Docker Hub 用户名）
docker tag fe-demo:latest yourusername/fe-demo:latest

# 3. 推送到 Docker Hub
docker push yourusername/fe-demo:latest

# 4. 其他人可以拉取
docker pull yourusername/fe-demo:latest
```

### 推送到私有仓库

```bash
# 1. 给镜像打标签（包含私有仓库地址）
docker tag fe-demo:latest registry.example.com/fe-demo:latest

# 2. 登录私有仓库
docker login registry.example.com

# 3. 推送
docker push registry.example.com/fe-demo:latest
```

### 推送到阿里云容器镜像服务

```bash
# 1. 登录阿里云镜像仓库
docker login --username=your-aliyun-account registry.cn-hangzhou.aliyuncs.com

# 2. 打标签
docker tag fe-demo:latest registry.cn-hangzhou.aliyuncs.com/namespace/fe-demo:latest

# 3. 推送
docker push registry.cn-hangzhou.aliyuncs.com/namespace/fe-demo:latest
```

## 🏗️ 完整的开发工作流

### 本地开发流程

```bash
# 1. 修改代码
vim src/App.tsx

# 2. 重新构建镜像
docker build -t fe-demo:latest .

# 3. 停止旧容器
docker stop my-fe-demo
docker rm my-fe-demo

# 4. 运行新容器
docker run -d -p 8080:80 --name my-fe-demo fe-demo:latest

# 5. 测试
open http://localhost:8080
```

### 使用 Makefile 简化流程

创建 `Makefile`:

```makefile
.PHONY: build run stop restart logs

build:
	docker build -t fe-demo:latest .

run:
	docker run -d -p 8080:80 --name fe-demo fe-demo:latest

stop:
	docker stop fe-demo || true
	docker rm fe-demo || true

restart: stop build run

logs:
	docker logs -f fe-demo

clean:
	docker stop fe-demo || true
	docker rm fe-demo || true
	docker rmi fe-demo:latest || true
```

使用：
```bash
make build    # 构建镜像
make run      # 运行容器
make restart  # 重启（停止→构建→运行）
make logs     # 查看日志
make clean    # 清理所有
```

## 🎯 生产环境最佳实践

### 使用版本标签

```bash
# 不要只用 latest
docker build -t fe-demo:v1.0.0 .
docker build -t fe-demo:v1.0.0 -t fe-demo:latest .
```

### 健康检查

在 `docker run` 时添加健康检查：

```bash
docker run -d -p 8080:80 \
  --name fe-demo \
  --health-cmd="curl -f http://localhost/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-retries=3 \
  fe-demo:latest
```

### 资源限制

```bash
docker run -d -p 8080:80 \
  --name fe-demo \
  --memory="256m" \
  --cpus="0.5" \
  fe-demo:latest
```

### 自动重启

```bash
docker run -d -p 8080:80 \
  --name fe-demo \
  --restart=unless-stopped \
  fe-demo:latest
```

## 📊 监控和日志

### 查看容器资源使用

```bash
# 实时查看资源使用
docker stats my-fe-demo

# 一次性查看
docker stats --no-stream my-fe-demo
```

### 导出日志

```bash
# 导出最近 100 行日志
docker logs --tail 100 my-fe-demo > container.log

# 导出所有日志
docker logs my-fe-demo > container-full.log
```

## 🐛 故障排查

### 容器无法启动

```bash
# 查看容器详细信息
docker inspect my-fe-demo

# 查看容器日志
docker logs my-fe-demo

# 尝试交互式运行
docker run -it --rm fe-demo:latest sh
```

### 端口被占用

```bash
# 查看端口使用情况
lsof -i :8080

# 使用其他端口
docker run -d -p 8081:80 --name fe-demo fe-demo:latest
```

### 镜像构建失败

```bash
# 查看构建缓存
docker builder prune

# 完全重新构建
docker build --no-cache -t fe-demo:latest .
```

## 📝 常见问题

### Q: 镜像在哪里？

**A**: 镜像保存在：
- **macOS**: `~/Library/Containers/com.docker.docker/`
- **Windows**: `C:\ProgramData\DockerDesktop\`
- **Linux**: `/var/lib/docker/`

你不需要直接访问这些目录，使用 `docker images` 命令即可。

### Q: 构建的镜像能在其他电脑用吗？

**A**: 可以，有两种方式：
1. **推送到镜像仓库**（推荐）
   ```bash
   docker push yourusername/fe-demo:latest
   # 其他电脑拉取
   docker pull yourusername/fe-demo:latest
   ```

2. **导出为文件**
   ```bash
   # 导出
   docker save fe-demo:latest -o fe-demo.tar

   # 在其他电脑导入
   docker load -i fe-demo.tar
   ```

### Q: 如何更新应用？

**A**:
```bash
# 1. 修改代码
# 2. 重新构建
docker build -t fe-demo:v2.0.0 .

# 3. 停止旧容器
docker stop my-fe-demo && docker rm my-fe-demo

# 4. 运行新版本
docker run -d -p 8080:80 --name my-fe-demo fe-demo:v2.0.0
```

### Q: Docker Desktop 占用空间太大？

**A**: 定期清理：
```bash
# 清理未使用的镜像
docker image prune -a

# 清理未使用的容器
docker container prune

# 清理所有未使用的资源
docker system prune -a --volumes
```

## 🎓 进阶阅读

- [Dockerfile 详细解析](./DOCKERFILE_DETAILED_EXPLANATION.md)
- [多阶段构建解析](./DOCKER_MULTISTAGE_EXPLAINED.md)
- [Kubernetes 部署指南](./DEPLOYMENT.md)

## 📚 有用的资源

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)

## 总结

恭喜！你现在已经：
- ✅ 成功构建了 Docker 镜像
- ✅ 镜像已保存在本地 Docker Desktop 中
- ✅ 学会了如何运行和管理容器
- ✅ 了解了如何推送到远程仓库

镜像就在你的本地 Docker 中，随时可以使用！🚀
