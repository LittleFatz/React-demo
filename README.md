# FE-DEMO 项目

一个基于 React + TypeScript + Vite 的前端项目，支持 Docker 和 Kubernetes 部署。

## 📁 项目结构

```
FE-DEMO/
├── 📚 docs/              # 所有文档
│   ├── DEPLOYMENT.md                      # 通用部署文档
│   ├── DOCKER_*.md                        # Docker 相关文档
│   ├── K8S_DEPLOYMENT_GUIDE.md            # Kubernetes 详细指南
│   ├── QUICK_START_K8S.md                 # K8s 快速开始
│   └── PORT_FORWARD_GUIDE.md              # 端口转发指南
│
├── 🔧 scripts/           # 部署和管理脚本
│   ├── deploy.sh                          # Docker 部署脚本
│   ├── deploy-k8s.sh                      # K8s 自动部署
│   ├── access-app.sh                      # 访问应用
│   ├── check-port-forwards.sh             # 查看端口转发
│   └── stop-port-forwards.sh              # 停止端口转发
│
├── 🐳 docker/            # Docker 相关文件
│   ├── Dockerfile                         # 生产环境 Dockerfile
│   ├── Dockerfile.single-stage            # 单阶段示例
│   └── nginx.conf                         # Nginx 配置
│
├── ☸️  k8s/              # Kubernetes 配置
│   ├── deployment.yaml                    # Deployment 配置
│   ├── service.yaml                       # Service 配置
│   ├── ingress.yaml                       # Ingress 配置
│   └── kustomization.yaml                 # Kustomize 配置
│
├── 💻 src/               # 源代码
│   └── ...                                # React 组件
│
├── 🎨 public/            # 静态资源
│   └── apple-touch-icon.svg
│
├── 📦 archive/           # 归档文件（与项目无关）
│   └── ...
│
└── ⚙️  配置文件           # 项目配置（根目录）
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── tailwind.config.ts
    └── index.html
```

---

## 🚀 快速开始

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### Docker 部署

```bash
# 构建镜像
docker build -f docker/Dockerfile -t fe-demo:latest .

# 运行容器
docker run -d -p 8080:80 --name fe-demo fe-demo:latest

# 访问
open http://localhost:8080
```

### Kubernetes 部署

```bash
# 快速部署（自动化脚本）
./scripts/deploy-k8s.sh

# 手动部署
kubectl apply -f k8s/

# 访问应用
./scripts/access-app.sh
```

---

## 📖 文档导航

### 新手入门

1. [快速开始 K8s 部署](docs/QUICK_START_K8S.md) ⭐ **推荐**
2. [Docker 使用指南](docs/DOCKER_USAGE_GUIDE.md)

### Docker 相关

- [Docker Build 概念](docs/DOCKER_BUILD_CONCEPT.md)
- [多阶段构建详解](docs/DOCKER_MULTISTAGE_EXPLAINED.md)
- [Dockerfile 详细解析](docs/DOCKERFILE_DETAILED_EXPLANATION.md)
- [Docker Run 命令详解](docs/DOCKER_RUN_EXPLAINED.md)
- [Docker PS 指南](docs/DOCKER_PS_GUIDE.md)

### Kubernetes 相关

- [K8s 部署完全指南](docs/K8S_DEPLOYMENT_GUIDE.md)
- [端口转发管理](docs/PORT_FORWARD_GUIDE.md)

### 通用部署

- [通用部署文档](docs/DEPLOYMENT.md)

---

## 🛠️ 常用命令

### Docker

```bash
# 构建镜像
docker build -f docker/Dockerfile -t fe-demo:latest .

# 查看镜像
docker images fe-demo

# 运行容器
docker run -d -p 8080:80 --name fe-demo fe-demo:latest

# 查看容器
docker ps -a

# 查看日志
docker logs fe-demo

# 停止删除
docker stop fe-demo && docker rm fe-demo
```

### Kubernetes

```bash
# 部署
kubectl apply -f k8s/

# 查看状态
kubectl get all
kubectl get pods
kubectl get svc

# 查看日志
kubectl logs -l app=fe-demo

# 端口转发
kubectl port-forward service/fe-demo-service 8080:80

# 删除
kubectl delete -f k8s/
```

### 脚本

```bash
# K8s 部署
./scripts/deploy-k8s.sh

# 访问应用
./scripts/access-app.sh

# 查看端口转发
./scripts/check-port-forwards.sh

# 停止端口转发
./scripts/stop-port-forwards.sh
```

---

## 🎯 项目特性

- ✅ React 18 + TypeScript
- ✅ Vite 构建工具
- ✅ Tailwind CSS
- ✅ Docker 多阶段构建
- ✅ Kubernetes 部署配置
- ✅ Nginx 反向代理
- ✅ 健康检查
- ✅ 自动化部署脚本

---

## 📊 技术栈

### 前端

- **框架**: React 18
- **语言**: TypeScript
- **构建工具**: Vite
- **样式**: Tailwind CSS
- **路由**: React Router DOM

### 部署

- **容器化**: Docker
- **编排**: Kubernetes
- **Web 服务器**: Nginx
- **镜像大小**: ~53MB

---

## 🔧 开发

### 目录说明

- **`src/`**: 源代码目录
- **`public/`**: 静态资源
- **`docker/`**: Docker 配置
- **`k8s/`**: Kubernetes 配置
- **`scripts/`**: 自动化脚本
- **`docs/`**: 项目文档

### 添加新功能

1. 在 `src/` 中开发
2. 本地测试：`npm run dev`
3. 构建：`npm run build`
4. Docker 测试：`docker build -f docker/Dockerfile -t fe-demo:test .`
5. 部署到 K8s：`./scripts/deploy-k8s.sh`

---

## 🐛 故障排查

### Docker 镜像无法构建

```bash
# 检查 Dockerfile
cat docker/Dockerfile

# 清理 Docker 缓存
docker system prune -a
```

### Kubernetes Pod 无法启动

```bash
# 查看 Pod 状态
kubectl get pods

# 查看详细信息
kubectl describe pod <pod-name>

# 查看日志
kubectl logs <pod-name>
```

### 无法访问应用

```bash
# 检查端口转发
./scripts/check-port-forwards.sh

# 重新启动端口转发
./scripts/access-app.sh
```

---

## 📚 相关资源

- [Docker 官方文档](https://docs.docker.com/)
- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [Vite 文档](https://vitejs.dev/)
- [React 文档](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 📝 版本历史

- **v0.1.0**: 初始项目
- **v1.0.0**: 添加 Docker 和 Kubernetes 支持
- **v1.1.0**: 重组项目结构，添加完整文档

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT

---

## 👤 作者

littlefatz

---

**提示**: 查看 `docs/` 目录获取详细文档！
