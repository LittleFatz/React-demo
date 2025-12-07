# Kustomize 实践练习

> 通过实际操作掌握 Kustomize

## 🎯 练习目标

通过完成这些练习，你将学会：
- 查看和理解 Kustomize 生成的配置
- 修改 overlay 配置
- 添加新的环境
- 使用 patch 修改配置
- 管理多环境部署

## 📋 练习前准备

确保你已经：
```bash
# 1. 阅读了 KUSTOMIZE_TUTORIAL.md
# 2. 当前目录在项目根目录
cd /Users/littlefatz/workspace/FE-DEMO

# 3. Kubernetes 集群运行中
kubectl cluster-info
```

---

## 练习 1: 预览配置（不部署）

### 目标
学会查看 Kustomize 生成的最终配置，而不实际部署。

### 步骤

**1.1 查看 DEV 环境完整配置**
```bash
kubectl kustomize k8s/overlays/dev/
```

**问题**：
- 找到 Deployment 的名称是什么？
- 答案应该是：`dev-fe-demo-deployment`

**1.2 只查看 Deployment 配置**
```bash
kubectl kustomize k8s/overlays/dev/ | grep -A 30 "kind: Deployment"
```

**问题**：
- DEV 环境有多少个副本？
- 答案应该是：1

**1.3 查看 Ingress 配置**
```bash
kubectl kustomize k8s/overlays/dev/ | grep -A 20 "kind: Ingress"
```

**问题**：
- Ingress 的域名是什么？
- 答案应该是：`dev.localhost`

### 验证
```bash
# 对比 DEV 和 UAT 的差异
echo "=== DEV Deployment ==="
kubectl kustomize k8s/overlays/dev/ | grep -A 5 "replicas:"

echo "=== UAT Deployment ==="
kubectl kustomize k8s/overlays/uat/ | grep -A 5 "replicas:"
```

---

## 练习 2: 修改副本数

### 目标
学会修改 overlay 配置并查看效果。

### 任务
将 DEV 环境的副本数从 1 改为 2。

### 步骤

**2.1 查看当前配置**
```bash
cat k8s/overlays/dev/kustomization.yaml | grep -A 2 "replicas:"
```

输出应该是：
```yaml
replicas:
  - name: fe-demo-deployment
    count: 1
```

**2.2 修改配置**

编辑 `k8s/overlays/dev/kustomization.yaml`，找到：
```yaml
replicas:
  - name: fe-demo-deployment
    count: 1              # 改为 2
```

改为：
```yaml
replicas:
  - name: fe-demo-deployment
    count: 2              # 已修改
```

**2.3 预览修改**
```bash
kubectl kustomize k8s/overlays/dev/ | grep -A 5 "replicas:"
```

应该看到：`replicas: 2`

**2.4 应用修改**
```bash
kubectl apply -k k8s/overlays/dev/
```

**2.5 验证**
```bash
kubectl get pods -n fe-demo-dev
```

应该看到 2 个 Pod 正在运行！

**2.6 改回去**

编辑配置改回 `count: 1`，然后：
```bash
kubectl apply -k k8s/overlays/dev/
kubectl get pods -n fe-demo-dev
```

---

## 练习 3: 修改域名

### 目标
学会使用 JSON Patch 修改配置。

### 任务
将 UAT 环境的域名从 `uat.localhost` 改为 `staging.localhost`。

### 步骤

**3.1 查看当前 Patch**
```bash
cat k8s/overlays/uat/kustomization.yaml
```

找到 patches 部分：
```yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: uat.localhost        # 这里
```

**3.2 修改配置**

编辑 `k8s/overlays/uat/kustomization.yaml`：
```yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: staging.localhost    # 改为 staging
```

**3.3 预览**
```bash
kubectl kustomize k8s/overlays/uat/ | grep -A 10 "kind: Ingress"
```

应该看到 `host: staging.localhost`

**3.4 应用**
```bash
kubectl apply -k k8s/overlays/uat/
```

**3.5 验证**
```bash
kubectl get ingress -n fe-demo-uat

# 测试访问
curl http://staging.localhost:8899 -s -o /dev/null -w "HTTP %{http_code}\n"
```

**3.6 改回去**

改回 `uat.localhost` 并重新应用。

---

## 练习 4: 添加环境变量

### 目标
学会添加新的配置到 Deployment。

### 任务
为 DEV 环境的容器添加环境变量 `ENV=dev` 和 `DEBUG=true`。

### 步骤

**4.1 创建 Patch**

编辑 `k8s/overlays/dev/kustomization.yaml`，在 patches 部分添加：

```yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: dev.localhost
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress

  # 添加新的 patch（注意格式）
  - patch: |-
      - op: add
        path: /spec/template/spec/containers/0/env
        value:
          - name: ENV
            value: dev
          - name: DEBUG
            value: "true"
    target:
      kind: Deployment
      name: fe-demo-deployment
```

**4.2 预览**
```bash
kubectl kustomize k8s/overlays/dev/ | grep -A 10 "env:"
```

应该看到：
```yaml
env:
- name: ENV
  value: dev
- name: DEBUG
  value: "true"
```

**4.3 应用**
```bash
kubectl apply -k k8s/overlays/dev/
```

**4.4 验证**
```bash
# 查看 Pod 中的环境变量
POD=$(kubectl get pods -n fe-demo-dev -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n fe-demo-dev $POD -- env | grep -E "ENV|DEBUG"
```

应该看到：
```
ENV=dev
DEBUG=true
```

---

## 练习 5: 创建新环境（TEST）

### 目标
从零创建一个新的环境配置。

### 任务
创建 TEST 环境，要求：
- 命名空间: `fe-demo-test`
- 前缀: `test-`
- 副本数: 2
- 域名: `test.localhost`
- 端口: 使用 8898（与 DEV 共享）

### 步骤

**5.1 创建目录**
```bash
mkdir -p k8s/overlays/test
```

**5.2 创建配置文件**

创建 `k8s/overlays/test/kustomization.yaml`：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: fe-demo-test

resources:
  - ../../base

namePrefix: test-

labels:
  - pairs:
      environment: test

replicas:
  - name: fe-demo-deployment
    count: 2

patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: test.localhost
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress
```

**5.3 预览**
```bash
kubectl kustomize k8s/overlays/test/
```

**5.4 创建命名空间**
```bash
kubectl create namespace fe-demo-test
```

**5.5 部署**
```bash
kubectl apply -k k8s/overlays/test/
```

**5.6 验证**
```bash
# 查看 Pods
kubectl get pods -n fe-demo-test

# 查看所有资源
kubectl get all -n fe-demo-test

# 测试访问
curl http://test.localhost:8898 -s -o /dev/null -w "HTTP %{http_code}\n"
```

**5.7 清理**
```bash
kubectl delete namespace fe-demo-test
```

---

## 练习 6: 对比环境差异

### 目标
学会比较不同环境的配置差异。

### 步骤

**6.1 导出配置到文件**
```bash
kubectl kustomize k8s/overlays/dev/ > /tmp/dev-config.yaml
kubectl kustomize k8s/overlays/uat/ > /tmp/uat-config.yaml
```

**6.2 对比副本数**
```bash
echo "=== DEV replicas ==="
grep "replicas:" /tmp/dev-config.yaml

echo "=== UAT replicas ==="
grep "replicas:" /tmp/uat-config.yaml
```

**6.3 对比资源名称**
```bash
echo "=== DEV names ==="
grep "name: dev-" /tmp/dev-config.yaml | head -5

echo "=== UAT names ==="
grep "name: uat-" /tmp/uat-config.yaml | head -5
```

**6.4 对比域名**
```bash
echo "=== DEV host ==="
grep "host:" /tmp/dev-config.yaml

echo "=== UAT host ==="
grep "host:" /tmp/uat-config.yaml
```

---

## 练习 7: 添加资源限制

### 目标
学会添加 CPU 和内存限制。

### 任务
为 UAT 环境添加资源限制：
- CPU 限制: 500m
- 内存限制: 512Mi
- CPU 请求: 100m
- 内存请求: 128Mi

### 步骤

**7.1 添加 Patch**

编辑 `k8s/overlays/uat/kustomization.yaml`，添加新的 patch：

```yaml
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: uat.localhost
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress

  # 添加资源限制
  - patch: |-
      - op: add
        path: /spec/template/spec/containers/0/resources
        value:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
    target:
      kind: Deployment
      name: fe-demo-deployment
```

**7.2 预览**
```bash
kubectl kustomize k8s/overlays/uat/ | grep -A 10 "resources:"
```

**7.3 应用**
```bash
kubectl apply -k k8s/overlays/uat/
```

**7.4 验证**
```bash
kubectl describe deployment uat-fe-demo-deployment -n fe-demo-uat | grep -A 5 "Limits:"
```

---

## 练习 8: 完整部署流程

### 目标
掌握完整的部署工作流程。

### 场景
你修改了代码，需要重新部署到 DEV 和 UAT 环境。

### 步骤

**8.1 重新构建镜像**
```bash
docker build -f docker/Dockerfile -t fe-demo:latest .
```

**8.2 预览变更**
```bash
kubectl diff -k k8s/overlays/dev/
kubectl diff -k k8s/overlays/uat/
```

**8.3 部署到 DEV**
```bash
kubectl apply -k k8s/overlays/dev/
```

**8.4 等待 DEV 就绪**
```bash
kubectl rollout status deployment/dev-fe-demo-deployment -n fe-demo-dev
```

**8.5 测试 DEV**
```bash
curl http://dev.localhost:8898 -s -o /dev/null -w "HTTP %{http_code}\n"
```

**8.6 部署到 UAT**
```bash
kubectl apply -k k8s/overlays/uat/
```

**8.7 等待 UAT 就绪**
```bash
kubectl rollout status deployment/uat-fe-demo-deployment -n fe-demo-uat
```

**8.8 测试 UAT**
```bash
curl http://uat.localhost:8899 -s -o /dev/null -w "HTTP %{http_code}\n"
```

**8.9 查看部署状态**
```bash
# 查看所有环境
kubectl get pods -A | grep fe-demo

# 查看日志
kubectl logs -n fe-demo-dev -l app=fe-demo --tail=20
kubectl logs -n fe-demo-uat -l app=fe-demo --tail=20
```

---

## 🎓 练习总结

完成这些练习后，你应该能够：

- ✅ 使用 `kubectl kustomize` 预览配置
- ✅ 修改 overlay 中的副本数
- ✅ 使用 JSON Patch 修改配置
- ✅ 添加环境变量和资源限制
- ✅ 创建新的环境
- ✅ 对比不同环境的差异
- ✅ 执行完整的部署流程

## 🚀 进阶挑战

如果你想进一步挑战，尝试：

1. **添加 ConfigMap**
   - 为不同环境创建不同的配置文件

2. **添加健康检查**
   - 为容器添加 liveness 和 readiness probe

3. **添加 HPA（水平自动扩缩容）**
   - 根据 CPU 使用率自动调整副本数

4. **使用 Secret**
   - 管理敏感配置（密码、API Key）

5. **添加 InitContainer**
   - 在主容器启动前执行初始化任务

## 📚 相关文档

- `KUSTOMIZE_TUTORIAL.md` - 完整教程
- `README.md` - 项目文档
- `ACCESS_GUIDE.md` - 访问指南

---

**祝你学习愉快！🎉**

如有问题，查看教程或尝试 `kubectl kustomize --help`
