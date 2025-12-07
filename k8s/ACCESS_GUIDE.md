# 多环境访问指南

## 🌐 访问地址

| 环境 | URL | 端口 | Pod 数量 |
|------|-----|------|----------|
| **DEV** | http://dev.localhost:8898 | 8898 | 1 |
| **UAT** | http://uat.localhost:8899 | 8899 | 2 |

## 🚀 快速开始

### 浏览器访问

直接在浏览器中打开以下地址：

- **DEV 环境**: [http://dev.localhost:8898](http://dev.localhost:8898)
- **UAT 环境**: [http://uat.localhost:8899](http://uat.localhost:8899)

### 命令行测试

```bash
# 测试 DEV 环境
curl http://dev.localhost:8898

# 测试 UAT 环境
curl http://uat.localhost:8899
```

## ✨ 优势

- ✅ **无需修改 hosts 文件**：`*.localhost` 域名自动解析到 `127.0.0.1`
- ✅ **端口隔离**：不同环境使用不同端口，互不干扰
- ✅ **环境独立**：各自的命名空间、资源、配置完全隔离
- ✅ **浏览器友好**：可直接在浏览器中访问，无需设置 Host header

## 🔧 Ingress Controller 配置

Ingress Controller 同时监听两个端口：

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller
```

输出：
```
NAME                       TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)
ingress-nginx-controller   LoadBalancer   10.98.94.132   localhost     8898:30663/TCP,443:31723/TCP,8899:30711/TCP
```

## 📊 环境详情

### DEV 环境

- **命名空间**: `fe-demo-dev`
- **域名**: `dev.localhost`
- **端口**: `8898`
- **Pod 副本数**: `1`
- **Deployment**: `dev-fe-demo-deployment`
- **Service**: `dev-fe-demo-service`
- **Ingress**: `dev-fe-demo-ingress`

### UAT 环境

- **命名空间**: `fe-demo-uat`
- **域名**: `uat.localhost`
- **端口**: `8899`
- **Pod 副本数**: `2`（负载均衡）
- **Deployment**: `uat-fe-demo-deployment`
- **Service**: `uat-fe-demo-service`
- **Ingress**: `uat-fe-demo-ingress`

## 🔍 验证部署

```bash
# 查看所有环境的 Pods
kubectl get pods -A | grep fe-demo

# 查看 DEV 环境
kubectl get all -n fe-demo-dev

# 查看 UAT 环境
kubectl get all -n fe-demo-uat

# 查看 Ingress
kubectl get ingress -n fe-demo-dev
kubectl get ingress -n fe-demo-uat
```

## 🛠️ 故障排查

### 无法访问

1. 检查 Pods 是否运行：
   ```bash
   kubectl get pods -n fe-demo-dev
   kubectl get pods -n fe-demo-uat
   ```

2. 检查 Ingress Controller：
   ```bash
   kubectl get pods -n ingress-nginx
   ```

3. 检查端口是否监听：
   ```bash
   lsof -i :8898
   lsof -i :8899
   ```

4. 测试端口连通性：
   ```bash
   curl -v http://dev.localhost:8898
   curl -v http://uat.localhost:8899
   ```

### 域名无法解析

如果 `*.localhost` 域名无法解析，可以临时使用 IP 地址：

```bash
# DEV
curl -H "Host: dev.localhost" http://127.0.0.1:8898

# UAT
curl -H "Host: uat.localhost" http://127.0.0.1:8899
```

## 📦 完整部署流程

```bash
# 1. 构建镜像
docker build -f docker/Dockerfile -t fe-demo:latest .

# 2. 创建命名空间（如果不存在）
kubectl create namespace fe-demo-dev
kubectl create namespace fe-demo-uat

# 3. 部署环境
kubectl apply -k k8s/overlays/dev/
kubectl apply -k k8s/overlays/uat/

# 4. 等待就绪
kubectl wait --for=condition=ready pod -l app=fe-demo -n fe-demo-dev --timeout=60s
kubectl wait --for=condition=ready pod -l app=fe-demo -n fe-demo-uat --timeout=60s

# 5. 访问应用
echo "DEV: http://dev.localhost:8898"
echo "UAT: http://uat.localhost:8899"
```

## 🗑️ 清理环境

```bash
# 删除 DEV
kubectl delete namespace fe-demo-dev

# 删除 UAT
kubectl delete namespace fe-demo-uat

# 或使用 kustomize
kubectl delete -k k8s/overlays/dev/
kubectl delete -k k8s/overlays/uat/
```
