# Kustomize 完全教程

> 基于当前 FE-DEMO 项目的实际配置讲解

## 🤔 什么是 Kustomize？

Kustomize 是 Kubernetes 原生的配置管理工具，用于**无需模板**的方式自定义 Kubernetes 配置。

### 核心思想

- **基础配置 (base)**: 所有环境共享的配置
- **覆盖配置 (overlays)**: 每个环境特定的修改
- **组合而非复制**: 通过 patch 方式修改，而不是复制整个文件

## 📁 当前项目结构解析

```
k8s/
├── base/                          # 基础配置（共享）
│   ├── deployment.yaml            # Deployment 定义
│   ├── service.yaml               # Service 定义
│   ├── ingress.yaml               # Ingress 定义
│   └── kustomization.yaml         # Base 的 Kustomize 配置
│
└── overlays/                      # 环境特定配置
    ├── dev/                       # DEV 环境
    │   └── kustomization.yaml     # DEV 的修改
    └── uat/                       # UAT 环境
        └── kustomization.yaml     # UAT 的修改
```

## 📝 第一步：理解 Base 配置

### base/deployment.yaml

这是所有环境共享的基础 Deployment 配置：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fe-demo-deployment
spec:
  replicas: 3                    # 默认 3 个副本（会被 overlay 覆盖）
  selector:
    matchLabels:
      app: fe-demo
  template:
    metadata:
      labels:
        app: fe-demo
    spec:
      containers:
      - name: fe-demo
        image: fe-demo:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
```

**关键点**：
- 这里定义了默认的 3 个副本
- DEV 和 UAT 会通过 overlay 修改副本数

### base/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fe-demo-service
spec:
  type: ClusterIP
  selector:
    app: fe-demo
  ports:
  - port: 80
    targetPort: 80
```

**关键点**：
- Service 配置在所有环境中相同
- 不需要修改，所以 overlay 不会覆盖它

### base/ingress.yaml

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fe-demo-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: fe-demo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fe-demo-service
            port:
              number: 80
  - host: localhost
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fe-demo-service
            port:
              number: 80
```

**关键点**：
- 定义了两个域名规则
- DEV 和 UAT 会修改这些域名

### base/kustomization.yaml

这是 Base 的 Kustomize 配置文件：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:                        # 包含的资源文件
  - deployment.yaml
  - service.yaml
  - ingress.yaml

labels:                           # 为所有资源添加标签
  - pairs:
      app: fe-demo
```

**解释**：
- `resources`: 列出所有要包含的 YAML 文件
- `labels`: 自动给所有资源添加 `app: fe-demo` 标签

## 🎨 第二步：理解 Overlay 配置

### overlays/dev/kustomization.yaml

DEV 环境的配置：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: fe-demo-dev              # 1️⃣ 设置命名空间

resources:                          # 2️⃣ 引用 base 配置
  - ../../base

namePrefix: dev-                    # 3️⃣ 资源名称前缀

labels:                             # 4️⃣ 添加环境标签
  - pairs:
      environment: dev

replicas:                           # 5️⃣ 修改副本数
  - name: fe-demo-deployment
    count: 1                        # DEV 只需要 1 个副本

patches:                            # 6️⃣ 修改特定配置
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: dev.localhost
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress
```

**逐项解释**：

#### 1️⃣ namespace: fe-demo-dev

- **作用**: 所有资源都会部署到 `fe-demo-dev` 命名空间
- **效果**: DEV 和 UAT 环境完全隔离

#### 2️⃣ resources: - ../../base

- **作用**: 引用 base 目录的所有配置
- **效果**: 继承 base 中的 deployment.yaml、service.yaml、ingress.yaml

#### 3️⃣ namePrefix: dev-

- **作用**: 给所有资源名称添加 `dev-` 前缀
- **效果**:
  - `fe-demo-deployment` → `dev-fe-demo-deployment`
  - `fe-demo-service` → `dev-fe-demo-service`
  - `fe-demo-ingress` → `dev-fe-demo-ingress`

#### 4️⃣ labels

- **作用**: 给所有资源添加 `environment: dev` 标签
- **效果**: 方便筛选和管理

#### 5️⃣ replicas

- **作用**: 覆盖 Deployment 的副本数
- **效果**: base 中的 3 副本改为 1 副本

#### 6️⃣ patches

- **作用**: 使用 JSON Patch 修改特定字段
- **效果**: 修改 Ingress 的域名配置
  - 第一个规则的 host 改为 `dev.localhost`
  - 删除第二个规则（原来的 localhost）

### overlays/uat/kustomization.yaml

UAT 环境配置（类似 DEV，但有不同）：

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: fe-demo-uat              # UAT 命名空间
resources:
  - ../../base
namePrefix: uat-                    # UAT 前缀
labels:
  - pairs:
      environment: uat
replicas:
  - name: fe-demo-deployment
    count: 2                        # UAT 需要 2 个副本
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: uat.localhost        # 不同的域名
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress
```

**与 DEV 的区别**：
- `namespace`: `fe-demo-uat` (不同)
- `namePrefix`: `uat-` (不同)
- `replicas count`: `2` (不同，DEV 是 1)
- `host`: `uat.localhost` (不同，DEV 是 dev.localhost)

## 🔍 第三步：看看 Kustomize 如何工作

### 预览生成的配置

不部署，只查看最终生成的 YAML：

```bash
# 预览 DEV 环境配置
kubectl kustomize k8s/overlays/dev/

# 预览 UAT 环境配置
kubectl kustomize k8s/overlays/uat/
```

### 实际演示 - DEV 环境

运行命令：
```bash
kubectl kustomize k8s/overlays/dev/ | grep -A 10 "kind: Deployment"
```

输出会显示：
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: fe-demo
    environment: dev              # ✅ 添加了环境标签
  name: dev-fe-demo-deployment    # ✅ 添加了 dev- 前缀
  namespace: fe-demo-dev          # ✅ 设置了命名空间
spec:
  replicas: 1                     # ✅ 从 3 改为 1
  selector:
    matchLabels:
      app: fe-demo
      environment: dev
```

**看到了吗？**
- 原来的 `fe-demo-deployment` → `dev-fe-demo-deployment`
- 原来的 `replicas: 3` → `replicas: 1`
- 添加了 `namespace: fe-demo-dev`
- 添加了 `environment: dev` 标签

## 🎯 第四步：实际部署

### 部署 DEV 环境

```bash
kubectl apply -k k8s/overlays/dev/
```

这一条命令等价于：
```bash
# 如果手动操作，需要：
kubectl create namespace fe-demo-dev
kubectl apply -f <生成的 deployment.yaml>
kubectl apply -f <生成的 service.yaml>
kubectl apply -f <生成的 ingress.yaml>
# 还要手动修改名称、副本数、域名...
```

### 验证部署

```bash
# 查看 DEV 环境
kubectl get all -n fe-demo-dev

# 输出：
# NAME                                          READY   STATUS    RESTARTS   AGE
# pod/dev-fe-demo-deployment-xxx                1/1     Running   0          1m
#
# NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
# service/dev-fe-demo-service   ClusterIP   10.100.184.201   <none>        80/TCP    1m
#
# NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/dev-fe-demo-deployment   1/1     1            1           1m
```

**注意**：
- ✅ 只有 1 个 Pod（replicas: 1）
- ✅ 所有资源都有 `dev-` 前缀
- ✅ 在 `fe-demo-dev` 命名空间

### 同时部署两个环境

```bash
kubectl apply -k k8s/overlays/dev/
kubectl apply -k k8s/overlays/uat/
```

查看所有环境：
```bash
kubectl get pods -A | grep fe-demo
```

输出：
```
fe-demo-dev   dev-fe-demo-deployment-xxx   1/1     Running   0          2m
fe-demo-uat   uat-fe-demo-deployment-xxx   1/1     Running   0          2m
fe-demo-uat   uat-fe-demo-deployment-yyy   1/1     Running   0          2m
```

**看！**
- DEV 有 1 个 Pod
- UAT 有 2 个 Pod
- 完全隔离，互不干扰

## 🔧 第五步：常见操作

### 1. JSON Patch 详解

Patches 使用 JSON Patch (RFC 6902) 格式：

```yaml
patches:
  - patch: |-
      - op: replace              # 操作类型
        path: /spec/rules/0/host # 要修改的路径
        value: dev.localhost     # 新值
      - op: remove               # 删除操作
        path: /spec/rules/1      # 要删除的路径
    target:                      # 指定要修改的资源
      kind: Ingress
      name: fe-demo-ingress
```

**常用操作**：
- `replace`: 替换字段值
- `add`: 添加新字段
- `remove`: 删除字段
- `copy`: 复制字段
- `move`: 移动字段

**路径说明**：
- `/spec/rules/0/host`: 第一个规则的 host 字段
- `/spec/rules/1`: 第二个规则（整个）
- 索引从 0 开始

### 2. 修改配置

#### 场景：DEV 也要 2 个副本

编辑 `k8s/overlays/dev/kustomization.yaml`：

```yaml
replicas:
  - name: fe-demo-deployment
    count: 2              # 改为 2
```

重新部署：
```bash
kubectl apply -k k8s/overlays/dev/
```

#### 场景：添加资源限制

在 overlay 中添加 patch：

```yaml
patches:
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

### 3. 添加新环境 (PROD)

创建 `k8s/overlays/prod/kustomization.yaml`：

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
    count: 5                      # 生产环境 5 个副本
patches:
  - patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: prod.example.com   # 真实域名
      - op: remove
        path: /spec/rules/1
    target:
      kind: Ingress
      name: fe-demo-ingress
```

部署：
```bash
kubectl create namespace fe-demo-prod
kubectl apply -k k8s/overlays/prod/
```

## 💡 Kustomize vs 其他方案

### 对比 Helm

| 特性 | Kustomize | Helm |
|------|-----------|------|
| 学习曲线 | ✅ 简单 | ❌ 复杂 |
| 模板语法 | ✅ 无需模板 | ❌ Go Template |
| Kubernetes 集成 | ✅ 内置 | ❌ 独立工具 |
| 适用场景 | 配置定制 | 包管理 |

### 对比复制文件

**传统方式**（不推荐）：
```
k8s/
├── dev-deployment.yaml
├── dev-service.yaml
├── dev-ingress.yaml
├── uat-deployment.yaml
├── uat-service.yaml
├── uat-ingress.yaml
└── prod-deployment.yaml
    prod-service.yaml
    prod-ingress.yaml
```

**问题**：
- ❌ 重复代码多
- ❌ 难以维护
- ❌ 修改 base 需要改多个文件

**Kustomize 方式**：
```
k8s/
├── base/           # 只维护一份
└── overlays/       # 只写差异
```

**优势**：
- ✅ 代码复用
- ✅ 易于维护
- ✅ 修改 base 自动影响所有环境

## 📚 实用技巧

### 1. 验证配置

```bash
# 预览而不部署
kubectl kustomize k8s/overlays/dev/

# 检查差异
kubectl diff -k k8s/overlays/dev/
```

### 2. 查看最终配置

```bash
# 导出到文件
kubectl kustomize k8s/overlays/dev/ > dev-config.yaml

# 查看特定资源
kubectl kustomize k8s/overlays/dev/ | grep -A 20 "kind: Deployment"
```

### 3. 调试 Patch

如果 patch 不生效：

```bash
# 查看完整输出
kubectl kustomize k8s/overlays/dev/ | less

# 检查语法
kubectl kustomize k8s/overlays/dev/ 2>&1 | grep -i error
```

### 4. 变量替换

使用 ConfigMap Generator：

```yaml
# kustomization.yaml
configMapGenerator:
  - name: app-config
    literals:
      - API_URL=https://api.dev.example.com
      - LOG_LEVEL=debug
```

## 🎓 最佳实践

1. **Base 保持通用**
   - 不包含环境特定配置
   - 使用合理的默认值

2. **Overlay 只写差异**
   - 不要重复 base 的内容
   - 使用 patch 而不是替换整个文件

3. **合理使用 namePrefix**
   - 避免资源名称冲突
   - 方便识别环境

4. **使用 namespace 隔离**
   - 每个环境独立的命名空间
   - 提高安全性

5. **测试配置**
   - 部署前先用 `kubectl kustomize` 预览
   - 使用 `kubectl diff` 检查变更

## 🔗 下一步

学完 Kustomize 后，你可以：

1. **添加 ConfigMap 管理**
   ```yaml
   configMapGenerator:
     - name: app-config
       files:
         - config.properties
   ```

2. **添加 Secret 管理**
   ```yaml
   secretGenerator:
     - name: app-secret
       literals:
         - password=secret123
   ```

3. **使用 commonAnnotations**
   ```yaml
   commonAnnotations:
     managed-by: kustomize
     version: "1.0.0"
   ```

4. **学习更高级的 Patch 技术**
   - Strategic Merge Patch
   - JSON 6902 Patch
   - Inline Patch

## 📖 参考资源

- [Kustomize 官方文档](https://kustomize.io/)
- [Kubernetes Kustomize 文档](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- 当前项目的 `k8s/README.md`
- 当前项目的 `k8s/ACCESS_GUIDE.md`

---

**恭喜！🎉** 你已经掌握了 Kustomize 的核心概念和实际应用！
