# Kubernetes 部署完全指南

## 📋 目录

1. [前提条件](#前提条件)
2. [启动 Kubernetes 集群](#启动-kubernetes-集群)
3. [准备 Docker 镜像](#准备-docker-镜像)
4. [部署到 Kubernetes](#部署到-kubernetes)
5. [验证部署](#验证部署)
6. [访问应用](#访问应用)
7. [管理和维护](#管理和维护)
8. [故障排查](#故障排查)

---

## 前提条件

### ✅ 需要安装的工具

- [x] Docker Desktop（已安装 ✅）
- [x] kubectl（已安装 ✅）
- [ ] Kubernetes 集群（需要启动）

### 检查安装

```bash
# 检查 Docker
docker --version

# 检查 kubectl
kubectl version --client

# 检查集群连接
kubectl cluster-info
```

---

## 启动 Kubernetes 集群

### 方法 1: Docker Desktop（推荐，用于本地开发）

#### 图形界面启动

1. **打开 Docker Desktop**
2. **点击设置图标** ⚙️（右上角）
3. **选择 Kubernetes**（左侧菜单）
4. **勾选 Enable Kubernetes** ✅
5. **点击 Apply & Restart**
6. **等待启动**（右下角显示 Kubernetes is running）

#### 等待时间

```
第一次启动: 2-5 分钟（需要下载镜像）
后续启动: 30-60 秒
```

#### 验证启动成功

```bash
# 查看集群信息
kubectl cluster-info

# 应该看到类似输出:
# Kubernetes control plane is running at https://kubernetes.docker.internal:6443
# CoreDNS is running at ...

# 查看节点
kubectl get nodes

# 应该看到:
# NAME             STATUS   ROLES           AGE   VERSION
# docker-desktop   Ready    control-plane   1d    v1.34.1
```

### 方法 2: Minikube（备选方案）

如果 Docker Desktop Kubernetes 有问题，可以使用 Minikube：

```bash
# 安装 Minikube（macOS）
brew install minikube

# 启动 Minikube
minikube start

# 查看状态
minikube status
```

### 常见启动问题

#### 问题 1: Kubernetes 启动卡住

**解决方法**:
```bash
# 重置 Kubernetes
# Docker Desktop → Preferences → Kubernetes → Reset Kubernetes Cluster
```

#### 问题 2: 资源不足

**解决方法**:
```bash
# 增加 Docker Desktop 资源
# Docker Desktop → Preferences → Resources
# 建议配置:
# - Memory: 4GB+
# - CPUs: 2+
# - Disk: 20GB+
```

---

## 准备 Docker 镜像

### 选项 1: 使用本地镜像（适合测试）

如果你已经构建了镜像：

```bash
# 检查镜像是否存在
docker images fe-demo

# 应该看到:
# REPOSITORY   TAG       SIZE
# fe-demo      latest    53.6MB
```

⚠️ **注意**: Docker Desktop 的 Kubernetes 可以直接使用本地 Docker 镜像！

修改 `k8s/deployment.yaml`:

```yaml
spec:
  template:
    spec:
      containers:
      - name: fe-demo
        image: fe-demo:latest
        imagePullPolicy: IfNotPresent  # 使用本地镜像
```

### 选项 2: 推送到镜像仓库（适合生产）

#### 推送到 Docker Hub

```bash
# 1. 登录 Docker Hub
docker login

# 2. 给镜像打标签
docker tag fe-demo:latest yourusername/fe-demo:latest

# 3. 推送
docker push yourusername/fe-demo:latest

# 4. 修改 deployment.yaml
# image: yourusername/fe-demo:latest
```

#### 推送到阿里云容器镜像服务

```bash
# 1. 登录阿里云
docker login --username=your-account registry.cn-hangzhou.aliyuncs.com

# 2. 打标签
docker tag fe-demo:latest registry.cn-hangzhou.aliyuncs.com/namespace/fe-demo:latest

# 3. 推送
docker push registry.cn-hangzhou.aliyuncs.com/namespace/fe-demo:latest

# 4. 修改 deployment.yaml
# image: registry.cn-hangzhou.aliyuncs.com/namespace/fe-demo:latest
```

---

## 部署到 Kubernetes

### 📂 部署文件说明

我们已经准备了以下文件：

```
k8s/
├── deployment.yaml      # Pod 部署配置
├── service.yaml         # 服务暴露配置
├── ingress.yaml         # 入口配置（可选）
└── kustomization.yaml   # 统一管理（可选）
```

### 🚀 部署步骤

#### 步骤 1: 检查配置文件

```bash
# 进入项目目录
cd /Users/littlefatz/workspace/FE-DEMO

# 查看部署文件
ls k8s/

# 检查 deployment.yaml
cat k8s/deployment.yaml
```

#### 步骤 2: 更新镜像配置（如果使用本地镜像）

编辑 `k8s/deployment.yaml`，确保：

```yaml
spec:
  template:
    spec:
      containers:
      - name: fe-demo
        image: fe-demo:latest          # 镜像名称
        imagePullPolicy: IfNotPresent  # 重要！使用本地镜像
```

#### 步骤 3: 部署应用

**方法 1: 逐个部署（推荐，便于理解）**

```bash
# 1. 创建 Deployment
kubectl apply -f k8s/deployment.yaml

# 输出:
# deployment.apps/fe-demo-deployment created

# 2. 创建 Service
kubectl apply -f k8s/service.yaml

# 输出:
# service/fe-demo-service created

# 3. 创建 Ingress（可选）
kubectl apply -f k8s/ingress.yaml

# 输出:
# ingress.networking.k8s.io/fe-demo-ingress created
```

**方法 2: 一次性部署**

```bash
# 部署所有资源
kubectl apply -f k8s/

# 输出:
# deployment.apps/fe-demo-deployment created
# ingress.networking.k8s.io/fe-demo-ingress created
# service/fe-demo-service created
```

**方法 3: 使用 Kustomize**

```bash
# 使用 kustomization.yaml
kubectl apply -k k8s/
```

---

## 验证部署

### 1️⃣ 检查 Deployment

```bash
# 查看 Deployment 状态
kubectl get deployments

# 应该看到:
# NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
# fe-demo-deployment   3/3     3            3           1m
```

**字段说明**:
- `READY`: 就绪的副本数 / 期望的副本数
- `UP-TO-DATE`: 已更新到最新配置的副本数
- `AVAILABLE`: 可用的副本数
- `AGE`: 部署存在的时间

### 2️⃣ 检查 Pods

```bash
# 查看 Pods
kubectl get pods

# 应该看到:
# NAME                                  READY   STATUS    RESTARTS   AGE
# fe-demo-deployment-abc123-xxxxx       1/1     Running   0          1m
# fe-demo-deployment-abc123-yyyyy       1/1     Running   0          1m
# fe-demo-deployment-abc123-zzzzz       1/1     Running   0          1m
```

**状态说明**:
- `Running`: 正常运行 ✅
- `Pending`: 等待调度
- `ContainerCreating`: 创建容器中
- `ImagePullBackOff`: 拉取镜像失败 ❌
- `CrashLoopBackOff`: 容器启动失败 ❌
- `Error`: 错误 ❌

### 3️⃣ 检查 Service

```bash
# 查看 Service
kubectl get services

# 或简写
kubectl get svc

# 应该看到:
# NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# fe-demo-service   ClusterIP   10.96.123.45    <none>        80/TCP    1m
```

### 4️⃣ 检查 Ingress（如果创建了）

```bash
# 查看 Ingress
kubectl get ingress

# 应该看到:
# NAME              CLASS   HOSTS                 ADDRESS     PORTS   AGE
# fe-demo-ingress   nginx   fe-demo.example.com   localhost   80      1m
```

### 5️⃣ 查看详细信息

```bash
# 查看 Deployment 详情
kubectl describe deployment fe-demo-deployment

# 查看 Pod 详情
kubectl describe pod <pod-name>

# 查看 Service 详情
kubectl describe service fe-demo-service

# 查看 Pod 日志
kubectl logs <pod-name>

# 实时查看日志
kubectl logs -f <pod-name>

# 查看所有 Pod 日志
kubectl logs -l app=fe-demo
```

### 6️⃣ 等待部署完成

```bash
# 等待 Deployment 就绪
kubectl rollout status deployment/fe-demo-deployment

# 应该看到:
# Waiting for deployment "fe-demo-deployment" rollout to finish: 0 of 3 updated replicas are available...
# Waiting for deployment "fe-demo-deployment" rollout to finish: 1 of 3 updated replicas are available...
# Waiting for deployment "fe-demo-deployment" rollout to finish: 2 of 3 updated replicas are available...
# deployment "fe-demo-deployment" successfully rolled out
```

---

## 访问应用

### 方法 1: Port Forward（最简单，推荐本地测试）

```bash
# 转发 Service 端口到本地
kubectl port-forward service/fe-demo-service 8080:80

# 输出:
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80

# 保持终端运行，打开浏览器访问:
# http://localhost:8080
```

**或者转发 Pod 端口**:

```bash
# 获取 Pod 名称
kubectl get pods

# 转发 Pod 端口
kubectl port-forward pod/<pod-name> 8080:80
```

### 方法 2: NodePort（暴露到宿主机端口）

修改 `k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fe-demo-service
spec:
  type: NodePort  # 改为 NodePort
  selector:
    app: fe-demo
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080  # 宿主机端口（30000-32767）
```

重新应用:

```bash
kubectl apply -f k8s/service.yaml

# 访问
# http://localhost:30080
```

### 方法 3: LoadBalancer（云环境）

修改 `k8s/service.yaml`:

```yaml
spec:
  type: LoadBalancer
```

```bash
kubectl apply -f k8s/service.yaml

# 查看外部 IP
kubectl get svc fe-demo-service

# Docker Desktop 会显示 localhost
```

### 方法 4: Ingress（推荐生产环境）

需要先安装 Ingress Controller。

#### 安装 Nginx Ingress Controller

```bash
# 安装
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# 等待就绪
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# 验证
kubectl get pods -n ingress-nginx
```

#### 配置 hosts 文件

编辑 `/etc/hosts`:

```bash
sudo nano /etc/hosts

# 添加:
127.0.0.1  fe-demo.example.com
```

#### 访问

```bash
# 浏览器访问
http://fe-demo.example.com
```

### 验证访问

```bash
# 使用 curl 测试
curl http://localhost:8080

# 应该看到 HTML 内容
# <!doctype html>
# <html lang="zh-Hans">
# ...
```

---

## 管理和维护

### 📊 监控状态

```bash
# 实时查看 Pods
watch kubectl get pods

# 查看资源使用
kubectl top nodes
kubectl top pods

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
```

### 🔄 更新应用

#### 更新镜像

```bash
# 方法 1: 重新构建并部署
docker build -t fe-demo:v2.0.0 .
kubectl set image deployment/fe-demo-deployment fe-demo=fe-demo:v2.0.0

# 方法 2: 修改 deployment.yaml 后重新应用
kubectl apply -f k8s/deployment.yaml

# 查看更新进度
kubectl rollout status deployment/fe-demo-deployment
```

#### 回滚

```bash
# 查看历史
kubectl rollout history deployment/fe-demo-deployment

# 回滚到上一个版本
kubectl rollout undo deployment/fe-demo-deployment

# 回滚到特定版本
kubectl rollout undo deployment/fe-demo-deployment --to-revision=2
```

### 📈 扩容/缩容

```bash
# 扩容到 5 个副本
kubectl scale deployment/fe-demo-deployment --replicas=5

# 缩容到 1 个副本
kubectl scale deployment/fe-demo-deployment --replicas=1

# 验证
kubectl get pods
```

### 🔍 调试

```bash
# 进入 Pod
kubectl exec -it <pod-name> -- sh

# 在 Pod 内执行命令
kubectl exec <pod-name> -- ls /usr/share/nginx/html

# 查看日志
kubectl logs <pod-name>

# 查看最近 100 行日志
kubectl logs --tail=100 <pod-name>

# 查看多个 Pod 的日志
kubectl logs -l app=fe-demo --tail=10
```

### 🗑️ 删除资源

```bash
# 删除 Deployment
kubectl delete deployment fe-demo-deployment

# 删除 Service
kubectl delete service fe-demo-service

# 删除 Ingress
kubectl delete ingress fe-demo-ingress

# 删除所有资源
kubectl delete -f k8s/

# 或使用标签删除
kubectl delete all -l app=fe-demo
```

---

## 故障排查

### 问题 1: Pod 一直处于 Pending 状态

**原因**: 资源不足或调度问题

**排查**:
```bash
# 查看详细信息
kubectl describe pod <pod-name>

# 查看事件
kubectl get events --field-selector involvedObject.name=<pod-name>
```

**解决**:
- 增加集群资源
- 检查资源限制配置

### 问题 2: ImagePullBackOff

**原因**: 无法拉取镜像

**排查**:
```bash
kubectl describe pod <pod-name>

# 查看 Events 部分，可能显示:
# Failed to pull image "fe-demo:latest": rpc error: code = Unknown
```

**解决**:
```bash
# 方法 1: 确保使用本地镜像
# 修改 deployment.yaml:
imagePullPolicy: IfNotPresent

# 方法 2: 推送镜像到仓库
docker push yourusername/fe-demo:latest

# 方法 3: 检查镜像是否存在
docker images fe-demo
```

### 问题 3: CrashLoopBackOff

**原因**: 容器启动后立即退出

**排查**:
```bash
# 查看日志
kubectl logs <pod-name>

# 查看之前的日志（如果重启了）
kubectl logs <pod-name> --previous

# 查看详细信息
kubectl describe pod <pod-name>
```

**解决**:
- 检查 Dockerfile 的 CMD 是否正确
- 确保使用 `daemon off;` (Nginx)
- 检查应用启动日志

### 问题 4: Service 无法访问

**排查**:
```bash
# 检查 Service
kubectl get svc fe-demo-service

# 检查 Endpoints
kubectl get endpoints fe-demo-service

# 应该看到 Pod IP
# NAME              ENDPOINTS                           AGE
# fe-demo-service   10.1.0.1:80,10.1.0.2:80,10.1.0.3:80 5m

# 如果 ENDPOINTS 是空的，说明 selector 不匹配
kubectl describe service fe-demo-service
```

**解决**:
- 确保 Service 的 selector 与 Deployment 的 labels 匹配
- 检查 Pod 是否正常运行

### 问题 5: 端口转发失败

**排查**:
```bash
# 检查 Pod 状态
kubectl get pods

# 检查 Pod 日志
kubectl logs <pod-name>
```

**解决**:
- 确保 Pod 处于 Running 状态
- 检查端口是否被占用
- 使用其他端口: `kubectl port-forward svc/fe-demo-service 8081:80`

---

## 📝 常用命令速查表

### 部署相关

```bash
kubectl apply -f k8s/                           # 部署所有资源
kubectl delete -f k8s/                          # 删除所有资源
kubectl rollout status deployment/fe-demo       # 查看部署状态
kubectl rollout history deployment/fe-demo      # 查看历史版本
kubectl rollout undo deployment/fe-demo         # 回滚部署
```

### 查看资源

```bash
kubectl get all                                 # 查看所有资源
kubectl get pods                                # 查看 Pods
kubectl get svc                                 # 查看 Services
kubectl get deployments                         # 查看 Deployments
kubectl get ingress                             # 查看 Ingress
```

### 详细信息

```bash
kubectl describe pod <pod-name>                 # Pod 详情
kubectl describe deployment <deployment-name>   # Deployment 详情
kubectl describe service <service-name>         # Service 详情
kubectl logs <pod-name>                         # 查看日志
kubectl logs -f <pod-name>                      # 实时查看日志
```

### 调试

```bash
kubectl exec -it <pod-name> -- sh               # 进入容器
kubectl port-forward svc/fe-demo-service 8080:80 # 端口转发
kubectl top pods                                # 资源使用
kubectl get events                              # 查看事件
```

### 管理

```bash
kubectl scale deployment/fe-demo --replicas=5   # 扩容
kubectl set image deployment/fe-demo fe-demo=fe-demo:v2 # 更新镜像
kubectl delete pod <pod-name>                   # 删除 Pod（会自动重建）
```

---

## 🎯 完整部署示例

假设你从零开始，完整流程：

```bash
# 1. 启动 Kubernetes（Docker Desktop）
# 通过 GUI 启动 Kubernetes

# 2. 验证集群
kubectl cluster-info
kubectl get nodes

# 3. 构建镜像
cd /Users/littlefatz/workspace/FE-DEMO
docker build -t fe-demo:latest .

# 4. 确认镜像配置（本地镜像）
# 编辑 k8s/deployment.yaml，确保:
# imagePullPolicy: IfNotPresent

# 5. 部署应用
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 6. 等待就绪
kubectl rollout status deployment/fe-demo-deployment

# 7. 验证
kubectl get pods
kubectl get svc

# 8. 访问应用
kubectl port-forward service/fe-demo-service 8080:80

# 9. 浏览器访问
# http://localhost:8080

# 10. 查看日志
kubectl logs -l app=fe-demo

# 完成！🎉
```

---

## 🎓 进阶主题

### ConfigMap 和 Secret

```bash
# 创建 ConfigMap
kubectl create configmap app-config --from-literal=API_URL=https://api.example.com

# 创建 Secret
kubectl create secret generic app-secret --from-literal=API_KEY=abc123

# 在 Deployment 中使用
# envFrom:
#   - configMapRef:
#       name: app-config
#   - secretRef:
#       name: app-secret
```

### 持久化存储

```yaml
# 创建 PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### 健康检查

已在 deployment.yaml 中配置:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 10
  periodSeconds: 5
```

---

## 📚 参考资源

- [Kubernetes 官方文档](https://kubernetes.io/docs/)
- [kubectl 速查表](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Docker Desktop Kubernetes](https://docs.docker.com/desktop/kubernetes/)

---

## 总结

恭喜！你现在应该能够：

- ✅ 启动 Kubernetes 集群
- ✅ 构建和准备 Docker 镜像
- ✅ 部署应用到 Kubernetes
- ✅ 验证和访问应用
- ✅ 管理和更新应用
- ✅ 排查常见问题

记住最重要的命令：
```bash
kubectl apply -f k8s/      # 部署
kubectl get pods           # 查看状态
kubectl logs <pod-name>    # 查看日志
kubectl port-forward svc/fe-demo-service 8080:80  # 访问
```

祝你部署顺利！🚀
