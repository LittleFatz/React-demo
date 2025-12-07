# Kubernetes 部署指南

本文档说明如何将 FE-DEMO 项目部署到 Kubernetes 集群。

## 前提条件

1. 已安装 Docker
2. 已安装 kubectl
3. 已配置好 Kubernetes 集群访问权限
4. (可选) 已安装 Helm 或 Kustomize

## 部署步骤

### 1. 构建 Docker 镜像

```bash
# 构建镜像
docker build -t fe-demo:latest .

# 如果使用远程镜像仓库,需要打标签并推送
docker tag fe-demo:latest your-registry/fe-demo:latest
docker push your-registry/fe-demo:latest
```

### 2. 更新 Kubernetes 配置

在 `k8s/deployment.yaml` 中更新镜像名称:

```yaml
image: your-registry/fe-demo:latest  # 替换为你的镜像地址
```

在 `k8s/ingress.yaml` 中更新域名:

```yaml
host: fe-demo.example.com  # 替换为你的域名
```

### 3. 部署到 Kubernetes

#### 方法一: 使用 kubectl 直接部署

```bash
# 创建命名空间(可选)
kubectl create namespace fe-demo

# 部署应用
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# 或者一次性部署所有资源
kubectl apply -f k8s/
```

#### 方法二: 使用 Kustomize 部署

```bash
kubectl apply -k k8s/
```

### 4. 验证部署

```bash
# 查看 Pod 状态
kubectl get pods -l app=fe-demo

# 查看 Service
kubectl get svc fe-demo-service

# 查看 Ingress
kubectl get ingress fe-demo-ingress

# 查看 Pod 日志
kubectl logs -l app=fe-demo

# 描述 Pod 详情
kubectl describe pod <pod-name>
```

### 5. 访问应用

#### 通过 Ingress 访问

如果配置了 Ingress,可以通过域名访问:
```
http://fe-demo.example.com
```

#### 通过 NodePort 访问

如果将 Service 类型改为 NodePort:

```bash
# 获取 NodePort
kubectl get svc fe-demo-service

# 访问
http://<node-ip>:<node-port>
```

#### 通过端口转发访问(用于测试)

```bash
kubectl port-forward svc/fe-demo-service 8080:80

# 在浏览器访问
http://localhost:8080
```

## 扩容和缩容

```bash
# 扩容到 5 个副本
kubectl scale deployment fe-demo-deployment --replicas=5

# 缩容到 2 个副本
kubectl scale deployment fe-demo-deployment --replicas=2
```

## 更新应用

```bash
# 构建新镜像
docker build -t fe-demo:v2 .
docker push your-registry/fe-demo:v2

# 更新部署
kubectl set image deployment/fe-demo-deployment fe-demo=your-registry/fe-demo:v2

# 查看滚动更新状态
kubectl rollout status deployment/fe-demo-deployment

# 如果需要回滚
kubectl rollout undo deployment/fe-demo-deployment
```

## 删除部署

```bash
# 删除所有资源
kubectl delete -f k8s/

# 或者使用标签删除
kubectl delete all -l app=fe-demo

# 删除命名空间(如果创建了)
kubectl delete namespace fe-demo
```

## 配置说明

### Deployment 配置

- **replicas**: 副本数量,默认为 3,可根据实际负载调整
- **resources**: 资源限制,可根据实际需求调整
- **livenessProbe**: 存活探针,检查容器是否正常运行
- **readinessProbe**: 就绪探针,检查容器是否准备好接收流量

### Service 配置

- **type**: 服务类型
  - ClusterIP: 仅集群内部访问(默认)
  - NodePort: 通过节点 IP 和端口访问
  - LoadBalancer: 通过云提供商的负载均衡器访问

### Ingress 配置

- 需要在集群中安装 Ingress Controller(如 nginx-ingress)
- 配置域名和 TLS 证书

## 最佳实践

1. **使用版本标签**: 不要使用 `latest` 标签,使用具体版本号
2. **资源限制**: 为容器设置合理的资源请求和限制
3. **健康检查**: 配置 liveness 和 readiness 探针
4. **滚动更新**: 使用滚动更新策略,确保零停机时间
5. **日志管理**: 配置日志收集和监控
6. **环境变量**: 使用 ConfigMap 和 Secret 管理配置
7. **多副本**: 运行多个副本以提高可用性

## 故障排查

```bash
# 查看 Pod 事件
kubectl describe pod <pod-name>

# 查看容器日志
kubectl logs <pod-name>

# 进入容器调试
kubectl exec -it <pod-name> -- sh

# 查看资源使用情况
kubectl top pods
kubectl top nodes
```

## 监控和日志

建议安装以下工具:

- Prometheus + Grafana: 监控和可视化
- ELK Stack 或 Loki: 日志收集和分析
- Jaeger: 分布式追踪

## 注意事项

1. 确保镜像已正确推送到镜像仓库
2. 如果使用私有镜像仓库,需要创建 imagePullSecret
3. 检查 Ingress Controller 是否已安装和配置
4. 确保集群有足够的资源运行应用
5. 在生产环境中使用 HTTPS
