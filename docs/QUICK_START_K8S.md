# Kubernetes 快速开始（5分钟部署）

## 🎯 前提条件

- ✅ Docker Desktop 已安装
- ✅ kubectl 已安装
- ❌ Kubernetes 集群需要启动 ← **你现在在这里**

---

## 🚀 快速部署（4 步完成）

### 第 1 步：启动 Kubernetes 集群 ⭐

**图形界面操作**：

1. 打开 **Docker Desktop** 应用
2. 点击右上角 **⚙️ 设置** (Settings)
3. 点击左侧 **Kubernetes**
4. **勾选** ✅ **Enable Kubernetes**
5. 点击 **Apply & Restart**
6. 等待启动（2-5分钟，右下角显示 🟢 Kubernetes is running）

**验证启动成功**：

```bash
# 在终端运行
kubectl cluster-info

# 应该看到：
# Kubernetes control plane is running at https://kubernetes.docker.internal:6443
# ✅ 说明启动成功

kubectl get nodes

# 应该看到：
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   1d    v1.34.1
# ✅ 节点就绪
```

---

### 第 2 步：自动部署（使用脚本）⭐ 推荐

```bash
# 进入项目目录
cd /Users/littlefatz/workspace/FE-DEMO

# 运行自动部署脚本
./deploy-k8s.sh
```

**脚本会自动完成**：
- ✅ 检查环境
- ✅ 检查/构建 Docker 镜像
- ✅ 部署到 Kubernetes
- ✅ 等待 Pods 就绪
- ✅ 显示部署状态

---

### 第 3 步：访问应用

**方法 1：使用脚本（最简单）**

```bash
./access-app.sh
```

然后浏览器打开：**http://localhost:8080**

**方法 2：手动端口转发**

```bash
kubectl port-forward service/fe-demo-service 8080:80
```

保持终端运行，浏览器打开：**http://localhost:8080**

---

### 第 4 步：验证部署

```bash
# 查看所有资源
kubectl get all

# 查看 Pods（应该有 3 个运行中）
kubectl get pods

# 应该看到：
# NAME                                  READY   STATUS    RESTARTS   AGE
# fe-demo-deployment-abc123-xxxxx       1/1     Running   0          1m
# fe-demo-deployment-abc123-yyyyy       1/1     Running   0          1m
# fe-demo-deployment-abc123-zzzzz       1/1     Running   0          1m

# 查看日志
kubectl logs -l app=fe-demo --tail=20
```

---

## 🛠️ 手动部署（如果不想用脚本）

### 1. 构建镜像（如果还没有）

```bash
docker build -t fe-demo:latest .
```

### 2. 部署到 Kubernetes

```bash
# 部署 Deployment
kubectl apply -f k8s/deployment.yaml

# 部署 Service
kubectl apply -f k8s/service.yaml
```

### 3. 等待就绪

```bash
# 等待 Pods 启动
kubectl rollout status deployment/fe-demo-deployment

# 应该看到：
# deployment "fe-demo-deployment" successfully rolled out
```

### 4. 访问应用

```bash
kubectl port-forward service/fe-demo-service 8080:80
```

---

## 📊 常用管理命令

### 查看状态

```bash
# 查看所有资源
kubectl get all

# 查看 Pods
kubectl get pods

# 查看 Pods 详细信息
kubectl get pods -o wide

# 查看 Service
kubectl get svc

# 查看 Deployment
kubectl get deployments
```

### 查看日志

```bash
# 查看所有 Pods 日志
kubectl logs -l app=fe-demo

# 实时查看日志
kubectl logs -l app=fe-demo -f

# 查看特定 Pod 日志
kubectl logs <pod-name>
```

### 扩容/缩容

```bash
# 扩容到 5 个副本
kubectl scale deployment/fe-demo-deployment --replicas=5

# 缩容到 1 个副本
kubectl scale deployment/fe-demo-deployment --replicas=1

# 验证
kubectl get pods
```

### 更新应用

```bash
# 重新构建镜像
docker build -t fe-demo:v2.0.0 .

# 更新镜像
kubectl set image deployment/fe-demo-deployment fe-demo=fe-demo:v2.0.0

# 查看更新进度
kubectl rollout status deployment/fe-demo-deployment
```

### 回滚

```bash
# 回滚到上一个版本
kubectl rollout undo deployment/fe-demo-deployment

# 查看历史
kubectl rollout history deployment/fe-demo-deployment
```

### 调试

```bash
# 进入 Pod
kubectl exec -it <pod-name> -- sh

# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看 Deployment 详情
kubectl describe deployment fe-demo-deployment

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
```

### 删除部署

```bash
# 删除所有资源
kubectl delete -f k8s/

# 或单独删除
kubectl delete deployment fe-demo-deployment
kubectl delete service fe-demo-service
```

---

## ⚠️ 常见问题

### 问题 1：Kubernetes 启动失败

**现象**：Docker Desktop 显示 Kubernetes starting... 很久

**解决**：
1. 重置 Kubernetes：Docker Desktop → Settings → Kubernetes → Reset Kubernetes Cluster
2. 增加资源：Docker Desktop → Settings → Resources（建议 4GB+ 内存）
3. 重启 Docker Desktop

### 问题 2：Pod 一直处于 ImagePullBackOff

**现象**：`kubectl get pods` 显示 ImagePullBackOff

**原因**：无法拉取镜像

**解决**：
```bash
# 确认镜像存在
docker images fe-demo

# 确认 deployment.yaml 中有：
# imagePullPolicy: IfNotPresent

# 重新部署
kubectl delete -f k8s/deployment.yaml
kubectl apply -f k8s/deployment.yaml
```

### 问题 3：Pod 一直处于 CrashLoopBackOff

**现象**：Pod 不断重启

**解决**：
```bash
# 查看日志
kubectl logs <pod-name>

# 查看之前的日志（重启前）
kubectl logs <pod-name> --previous

# 查看详情
kubectl describe pod <pod-name>

# 常见原因：
# - Dockerfile CMD 配置错误
# - 应用启动失败
# - 健康检查失败
```

### 问题 4：无法访问应用

**检查清单**：
```bash
# 1. 检查 Pod 是否运行
kubectl get pods
# 状态应该是 Running

# 2. 检查 Service
kubectl get svc fe-demo-service
# 应该有 CLUSTER-IP

# 3. 检查 Endpoints
kubectl get endpoints fe-demo-service
# 应该有 Pod IP

# 4. 查看 Pod 日志
kubectl logs -l app=fe-demo

# 5. 重新端口转发
kubectl port-forward service/fe-demo-service 8080:80
```

---

## 🎯 完整流程检查清单

- [ ] Docker Desktop 已启动
- [ ] Kubernetes 已启用（Docker Desktop 右下角显示 🟢）
- [ ] 运行 `kubectl cluster-info` 成功
- [ ] 运行 `kubectl get nodes` 显示 Ready
- [ ] 运行 `docker images fe-demo` 可以看到镜像
- [ ] 运行 `./deploy-k8s.sh` 部署成功
- [ ] 运行 `kubectl get pods` 显示 3 个 Running
- [ ] 运行 `./access-app.sh` 或 `kubectl port-forward`
- [ ] 浏览器访问 http://localhost:8080 正常

---

## 📚 更多资源

- [完整部署指南](./K8S_DEPLOYMENT_GUIDE.md) - 详细的部署文档
- [Docker 使用指南](./DOCKER_USAGE_GUIDE.md) - Docker 命令参考
- [部署文档](./DEPLOYMENT.md) - 通用部署说明

---

## 🎉 总结

最简单的 3 个命令：

```bash
# 1. 启动 Kubernetes（通过 Docker Desktop GUI）

# 2. 部署
./deploy-k8s.sh

# 3. 访问
./access-app.sh
```

就这么简单！🚀

如果遇到问题，查看日志：
```bash
kubectl logs -l app=fe-demo
kubectl describe pod <pod-name>
```
