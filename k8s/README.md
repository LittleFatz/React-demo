# Kubernetes 多环境部署配置

本项目使用 Kustomize 管理多环境部署。

## 📁 目录结构

```
k8s/
├── base/                       # 基础配置（共享）
│   ├── deployment.yaml        # Deployment 定义
│   ├── service.yaml           # Service 定义
│   ├── ingress.yaml           # Ingress 定义
│   └── kustomization.yaml     # Base kustomization
│
├── overlays/                   # 环境特定配置
│   ├── dev/                   # DEV 环境
│   │   └── kustomization.yaml # 1 个 Pod 副本
│   └── uat/                   # UAT 环境
│       └── kustomization.yaml # 2 个 Pod 副本
│
├── deployment.yaml            # （保留，向后兼容）
├── service.yaml               # （保留，向后兼容）
├── ingress.yaml               # （保留，向后兼容）
└── kustomization.yaml         # （保留，向后兼容）
```

## 🚀 快速部署

### DEV 环境（1 个 Pod）

```bash
# 部署 DEV 环境
kubectl apply -k k8s/overlays/dev/

# 查看 DEV 环境资源
kubectl get all -n fe-demo-dev

# 访问 DEV 环境（端口 8898）
curl http://dev.localhost:8898
# 或在浏览器访问：http://dev.localhost:8898
```

### UAT 环境（2 个 Pod）

```bash
# 部署 UAT 环境
kubectl apply -k k8s/overlays/uat/

# 查看 UAT 环境资源
kubectl get all -n fe-demo-uat

# 访问 UAT 环境（端口 8899）
curl http://uat.localhost:8899
# 或在浏览器访问：http://uat.localhost:8899
```

### 同时部署两个环境

```bash
# 部署 DEV 和 UAT
kubectl apply -k k8s/overlays/dev/
kubectl apply -k k8s/overlays/uat/

# 查看所有环境
kubectl get pods -A | grep fe-demo
```

## 🔧 环境配置说明

| 环境 | 命名空间 | Pod 副本数 | Name Prefix | 域名 | Ingress 端口 |
|-----|---------|-----------|-------------|------|--------------|
| **DEV** | fe-demo-dev | 1 | dev- | dev.localhost | 8898 |
| **UAT** | fe-demo-uat | 2 | uat- | uat.localhost | 8899 |

### 资源命名规则

**DEV 环境：**
- Deployment: `dev-fe-demo-deployment`
- Service: `dev-fe-demo-service`
- Ingress: `dev-fe-demo-ingress`

**UAT 环境：**
- Deployment: `uat-fe-demo-deployment`
- Service: `uat-fe-demo-service`
- Ingress: `uat-fe-demo-ingress`

## 📊 查看部署状态

```bash
# 查看 DEV 环境
kubectl get all -n fe-demo-dev
kubectl get pods -n fe-demo-dev
kubectl logs -n fe-demo-dev -l app=fe-demo

# 查看 UAT 环境
kubectl get all -n fe-demo-uat
kubectl get pods -n fe-demo-uat
kubectl logs -n fe-demo-uat -l app=fe-demo

# 查看 Ingress
kubectl get ingress -n fe-demo-dev
kubectl get ingress -n fe-demo-uat
```

## 🗑️ 删除部署

```bash
# 删除 DEV 环境
kubectl delete -k k8s/overlays/dev/

# 删除 UAT 环境
kubectl delete -k k8s/overlays/uat/

# 或者直接删除命名空间（会删除所有资源）
kubectl delete namespace fe-demo-dev
kubectl delete namespace fe-demo-uat
```

## 🔄 更新部署

修改代码后重新部署：

```bash
# 1. 重新构建镜像
docker build -f docker/Dockerfile -t fe-demo:latest .

# 2. 重启 Pod（触发更新）
kubectl rollout restart deployment/dev-fe-demo-deployment -n fe-demo-dev
kubectl rollout restart deployment/uat-fe-demo-deployment -n fe-demo-uat

# 3. 查看滚动更新状态
kubectl rollout status deployment/dev-fe-demo-deployment -n fe-demo-dev
kubectl rollout status deployment/uat-fe-demo-deployment -n fe-demo-uat
```

## ✨ 添加新环境

如果需要添加新环境（如 PROD），创建 `overlays/prod/kustomization.yaml`：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: fe-demo-prod

resources:
  - ../../base

namePrefix: prod-

labels:
  - pairs:
      environment: prod

replicas:
  - name: fe-demo-deployment
    count: 3  # 生产环境 3 个副本

patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: fe-demo-prod.example.com
      - op: replace
        path: /spec/rules/1/host
        value: localhost
    target:
      kind: Ingress
      name: fe-demo-ingress
```

然后部署：
```bash
kubectl apply -k k8s/overlays/prod/
```

## 📝 验证配置

在部署前预览生成的 YAML：

```bash
# 预览 DEV 配置
kubectl kustomize k8s/overlays/dev/

# 预览 UAT 配置
kubectl kustomize k8s/overlays/uat/
```

## 🎯 最佳实践

1. **基础配置放在 base/**：所有环境共享的配置
2. **环境特定配置放在 overlays/**：只包含差异部分
3. **使用 namePrefix**：避免不同环境资源冲突
4. **使用 namespace**：隔离不同环境
5. **使用 labels**：便于过滤和管理

## 🔗 相关命令

```bash
# 查看所有命名空间的 Pods
kubectl get pods -A | grep fe-demo

# 端口转发访问 DEV
kubectl port-forward -n fe-demo-dev service/dev-fe-demo-service 8080:80

# 端口转发访问 UAT
kubectl port-forward -n fe-demo-uat service/uat-fe-demo-service 8081:80

# 查看资源使用情况
kubectl top pods -n fe-demo-dev
kubectl top pods -n fe-demo-uat
```
