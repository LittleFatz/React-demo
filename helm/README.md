# Helm 部署指南

## 📁 Chart 结构

```
helm/fe-demo/
├── Chart.yaml              # Chart 元数据
├── values.yaml             # 默认配置（所有环境共享）
├── values-dev.yaml         # DEV 环境配置
├── values-uat.yaml         # UAT 环境配置
└── templates/              # 模板目录
    ├── deployment.yaml     # Deployment 模板
    ├── service.yaml        # Service 模板
    └── ingress.yaml        # Ingress 模板
```

## 🚀 快速开始

> **💡 重要提示**：以下命令假设你在项目根目录（`FE-DEMO/`）执行。所有路径都相对于当前工作目录。

### 部署 DEV 环境

```bash
# 确保在项目根目录
cd /Users/littlefatz/workspace/FE-DEMO

# 部署 DEV 环境
helm install dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml \
  --namespace fe-demo-dev
```

### 部署 UAT 环境

```bash
helm install uat-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-uat.yaml \
  --namespace fe-demo-uat
```

## 📊 常用命令

### 查看

```bash
# 查看所有 Releases
helm list -A

# 查看 Release 状态
helm status dev-fe-demo -n fe-demo-dev

# 查看配置值
helm get values dev-fe-demo -n fe-demo-dev

# 查看部署的资源
helm get manifest dev-fe-demo -n fe-demo-dev
```

### 升级

```bash
# 升级 Release
helm upgrade dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml \
  --namespace fe-demo-dev

# 查看升级历史
helm history dev-fe-demo -n fe-demo-dev
```

### 回滚

```bash
# 回滚到上一个版本
helm rollback dev-fe-demo -n fe-demo-dev

# 回滚到特定版本
helm rollback dev-fe-demo 1 -n fe-demo-dev
```

### 删除

```bash
# 删除 DEV 环境
helm uninstall dev-fe-demo -n fe-demo-dev

# 删除 UAT 环境
helm uninstall uat-fe-demo -n fe-demo-uat
```

### 调试

```bash
# 检查 Chart 语法
helm lint helm/fe-demo/

# 渲染模板（不部署）
helm template dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml

# 模拟安装（dry run）
helm install dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml \
  --namespace fe-demo-dev \
  --dry-run
```

## 🌍 环境配置

### DEV 环境

- **副本数**: 1
- **域名**: dev.localhost
- **端口**: 8898
- **配置文件**: `values-dev.yaml`

### UAT 环境

- **副本数**: 2
- **域名**: uat.localhost
- **端口**: 8899
- **配置文件**: `values-uat.yaml`

## 🎨 自定义配置

### 修改副本数

编辑 `values-dev.yaml`:

```yaml
replicaCount: 3  # 修改为 3 个副本
```

然后升级：

```bash
helm upgrade dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml \
  --namespace fe-demo-dev
```

### 修改镜像版本

编辑 `values.yaml` 或环境特定的 values 文件:

```yaml
image:
  repository: fe-demo
  tag: v2.0.0  # 修改版本
  pullPolicy: IfNotPresent
```

### 添加资源限制

编辑 values 文件:

```yaml
resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

## 📚 Go Template 语法速查

```yaml
# 读取值
{{ .Values.replicaCount }}      # 从 values.yaml 读取
{{ .Release.Name }}              # Release 名称
{{ .Chart.Name }}                # Chart 名称

# 条件判断
{{- if .Values.ingress.enabled }}
...
{{- end }}

# 循环
{{- range .Values.items }}
- {{ . }}
{{- end }}

# 函数
{{ .Values.name | quote }}       # 加引号
{{ .Values.name | upper }}       # 转大写
{{ toYaml .Values.resources | nindent 10 }}  # YAML 格式化
```

## 🔍 故障排查

### 问题 1: Chart 语法错误

```bash
# 检查语法
helm lint helm/fe-demo/
```

### 问题 2: 查看渲染后的 YAML

```bash
# 渲染模板
helm template dev-fe-demo helm/fe-demo/ \
  --values helm/fe-demo/values-dev.yaml
```

### 问题 3: Pod 启动失败

```bash
# 查看 Release 状态
helm status dev-fe-demo -n fe-demo-dev

# 查看 Pod 日志
kubectl logs -n fe-demo-dev -l app=fe-demo
```

### 问题 4: 升级失败需要回滚

```bash
# 查看历史
helm history dev-fe-demo -n fe-demo-dev

# 回滚
helm rollback dev-fe-demo -n fe-demo-dev
```

## 📖 参考资源

- [Helm 官方文档](https://helm.sh/docs/)
- [Go Template 文档](https://pkg.go.dev/text/template)
- [Helm Chart 最佳实践](https://helm.sh/docs/chart_best_practices/)

## 🔍 路径解析说明

### -f 参数的路径规则

**核心原则**：所有路径都相对于**当前工作目录** (pwd)

### 场景 1: 在项目根目录执行（推荐）

```bash
$ pwd
/Users/littlefatz/workspace/FE-DEMO

# ✓ 正确
$ helm install dev-fe-demo helm/fe-demo/ \
    -f helm/fe-demo/values-dev.yaml \
    -n fe-demo-dev

# ✗ 错误（找不到文件）
$ helm install dev-fe-demo helm/fe-demo/ \
    -f values-dev.yaml \
    -n fe-demo-dev
```

### 场景 2: 在 Chart 目录内执行

```bash
$ pwd
/Users/littlefatz/workspace/FE-DEMO/helm/fe-demo

# ✓ 正确（Chart 路径用 .）
$ helm install dev-fe-demo . \
    -f values-dev.yaml \
    -n fe-demo-dev
```

### 最佳实践

1. **推荐**：始终在项目根目录执行，使用完整相对路径
2. 避免混淆：不要假设 Helm 会自动在 Chart 目录中查找 values 文件
3. CI/CD：使用绝对路径或确保脚本中明确设置工作目录

### 常见错误

```bash
# ❌ 错误 1: 路径不正确
Error: open values-dev.yaml: no such file or directory

# 原因：当前目录没有这个文件，需要完整路径
# 解决：-f helm/fe-demo/values-dev.yaml

# ❌ 错误 2: Chart 路径错误  
Error: path "fe-demo" not found

# 原因：Chart 目录不在当前目录
# 解决：使用正确的相对或绝对路径
```
