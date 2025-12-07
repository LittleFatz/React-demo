# 快速参考指南

> 目录已重新整理，这是新结构下的快速使用指南

---

## 📁 新目录结构

```
FE-DEMO/
├── docs/              # 📚 所有文档
├── scripts/           # 🔧 所有脚本
├── docker/            # 🐳 Docker 文件
├── k8s/              # ☸️ Kubernetes 配置
├── src/              # 💻 源代码
├── public/           # 🎨 静态资源
├── archive/          # 📦 归档（不使用）
└── 配置文件           # ⚙️ 项目配置
```

---

## 🚀 常用操作（已更新路径）

### Docker 操作

```bash
# 构建镜像（注意路径变化）
docker build -f docker/Dockerfile -t fe-demo:latest .

# 运行容器
docker run -d -p 8080:80 --name fe-demo fe-demo:latest

# 查看镜像
docker images fe-demo

# 查看容器
docker ps -a
```

### Kubernetes 操作

```bash
# 一键部署（推荐）⭐ 包含镜像构建、Ingress配置等
./scripts/quick-deploy.sh

# 使用 Kustomize 部署（最简单）
kubectl apply -k k8s/

# 传统脚本部署
./scripts/deploy-k8s.sh

# 手动部署
kubectl apply -f k8s/

# 一键删除所有资源
./scripts/quick-remove.sh

# 访问应用
./scripts/access-app.sh

# 查看端口转发
./scripts/check-port-forwards.sh

# 停止端口转发
./scripts/stop-port-forwards.sh
```

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建
npm run build
```

---

## 📖 文档查阅

所有文档都在 `docs/` 目录：

```bash
# 查看 Kubernetes 快速开始
cat docs/QUICK_START_K8S.md

# 查看 Docker 使用指南
cat docs/DOCKER_USAGE_GUIDE.md

# 查看端口转发指南
cat docs/PORT_FORWARD_GUIDE.md

# 列出所有文档
ls docs/
```

---

## 🔧 脚本使用

所有脚本都在 `scripts/` 目录：

```bash
# Kubernetes 部署
./scripts/deploy-k8s.sh

# Docker 部署
./scripts/deploy.sh

# 访问应用（端口转发）
./scripts/access-app.sh

# 查看所有端口转发
./scripts/check-port-forwards.sh

# 停止端口转发
./scripts/stop-port-forwards.sh
```

---

## ⚠️ 重要变化

### 1. Dockerfile 路径变化

**之前**:
```bash
docker build -t fe-demo:latest .
```

**现在**:
```bash
docker build -f docker/Dockerfile -t fe-demo:latest .
```

### 2. nginx.conf 路径变化

位置从根目录移到了 `docker/nginx.conf`

Dockerfile 中的引用已自动更新（相对路径）

### 3. 脚本路径变化

**之前**:
```bash
./deploy-k8s.sh
./access-app.sh
```

**现在**:
```bash
./scripts/deploy-k8s.sh
./scripts/access-app.sh
```

### 4. 文档路径变化

**之前**: 文档在根目录
**现在**: 所有文档在 `docs/` 目录

---

## 💡 快捷别名（可选）

将以下内容添加到 `~/.bashrc` 或 `~/.zshrc`:

```bash
# FE-DEMO 项目别名
alias fe-build='docker build -f docker/Dockerfile -t fe-demo:latest .'
alias fe-deploy='./scripts/deploy-k8s.sh'
alias fe-access='./scripts/access-app.sh'
alias fe-check='./scripts/check-port-forwards.sh'
alias fe-stop='./scripts/stop-port-forwards.sh'
alias fe-dev='npm run dev'
```

使用：
```bash
fe-build    # 构建 Docker 镜像
fe-deploy   # 部署到 K8s
fe-access   # 访问应用
```

---

## 🎯 完整工作流

### 开发 → Docker → Kubernetes

```bash
# 1. 本地开发
npm run dev

# 2. 构建镜像
docker build -f docker/Dockerfile -t fe-demo:latest .

# 3. 测试镜像
docker run -d -p 8080:80 --name fe-demo-test fe-demo:latest
curl http://localhost:8080
docker stop fe-demo-test && docker rm fe-demo-test

# 4. 部署到 K8s
./scripts/deploy-k8s.sh

# 5. 访问应用
./scripts/access-app.sh
```

---

## 📊 目录文件统计

```
docs/      : 11 个文档文件
scripts/   : 5 个脚本
docker/    : 3 个文件（Dockerfile + nginx.conf + 示例）
k8s/       : 4 个配置文件
public/    : 静态资源
archive/   : 归档文件（不使用）
```

---

## 🆘 需要帮助？

1. 查看 [README.md](README.md)
2. 查看 [docs/QUICK_START_K8S.md](docs/QUICK_START_K8S.md)
3. 查看其他 `docs/` 下的文档

---

## ✅ 验证整理结果

```bash
# 查看目录结构
ls -la

# 应该看到：
# ✅ docs/
# ✅ scripts/
# ✅ docker/
# ✅ k8s/
# ✅ src/
# ✅ public/
# ✅ archive/
# ✅ README.md
# ✅ package.json
# ✅ 其他配置文件

# 验证脚本可执行
ls -l scripts/

# 应该都有执行权限 (x)
```

---

**🎉 目录整理完成！现在项目结构更清晰了！**
