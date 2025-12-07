#!/bin/bash

# Kubernetes 快速部署脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        error "$1 未安装，请先安装"
    fi
}

# 步骤 1: 检查环境
step "1. 检查环境"
info "检查 kubectl..."
check_command kubectl
info "✓ kubectl 已安装"

info "检查 docker..."
check_command docker
info "✓ Docker 已安装"

# 步骤 2: 检查 Kubernetes 集群
step "2. 检查 Kubernetes 集群"
if ! kubectl cluster-info &> /dev/null; then
    error "Kubernetes 集群未运行！

请启动 Kubernetes:
1. 打开 Docker Desktop
2. 点击设置 ⚙️
3. 选择 Kubernetes
4. 勾选 Enable Kubernetes
5. 点击 Apply & Restart
6. 等待启动完成后重新运行此脚本"
fi

info "✓ Kubernetes 集群运行中"

# 显示集群信息
kubectl cluster-info | head -n 2

# 步骤 3: 检查镜像
step "3. 检查 Docker 镜像"
if ! docker images fe-demo:latest --format "{{.Repository}}" | grep -q "fe-demo"; then
    warn "镜像 fe-demo:latest 不存在"
    info "开始构建镜像..."
    docker build -t fe-demo:latest . || error "镜像构建失败"
    info "✓ 镜像构建成功"
else
    info "✓ 镜像 fe-demo:latest 已存在"
fi

# 步骤 4: 更新部署配置（确保使用本地镜像）
step "4. 更新部署配置"
if ! grep -q "imagePullPolicy: IfNotPresent" k8s/deployment.yaml; then
    warn "正在更新 deployment.yaml 以使用本地镜像..."
    # 备份原文件
    cp k8s/deployment.yaml k8s/deployment.yaml.bak
    # 添加 imagePullPolicy
    if grep -q "image: fe-demo:latest" k8s/deployment.yaml; then
        sed -i '' '/image: fe-demo:latest/a\
        imagePullPolicy: IfNotPresent' k8s/deployment.yaml
        info "✓ 已更新配置"
    fi
else
    info "✓ 配置已正确设置"
fi

# 步骤 5: 部署到 Kubernetes
step "5. 部署到 Kubernetes"
info "部署 Deployment..."
kubectl apply -f k8s/deployment.yaml

info "部署 Service..."
kubectl apply -f k8s/service.yaml

info "✓ 部署完成"

# 步骤 6: 等待部署就绪
step "6. 等待部署就绪"
info "等待 Pods 启动..."
kubectl wait --for=condition=ready pod -l app=fe-demo --timeout=120s || warn "等待超时，请检查 Pod 状态"

# 步骤 7: 验证部署
step "7. 验证部署状态"
echo ""
info "Deployment 状态:"
kubectl get deployments fe-demo-deployment

echo ""
info "Pod 状态:"
kubectl get pods -l app=fe-demo

echo ""
info "Service 状态:"
kubectl get service fe-demo-service

# 步骤 8: 访问说明
echo ""
step "8. 访问应用"
cat << 'EOF'

🎉 部署成功！

现在你可以通过以下方式访问应用：

方法 1: 端口转发（推荐）
---------------------------------------
运行以下命令：
  kubectl port-forward service/fe-demo-service 8080:80

然后在浏览器访问：
  http://localhost:8080

按 Ctrl+C 停止转发

方法 2: 使用脚本
---------------------------------------
运行以下命令：
  ./access-app.sh

常用管理命令：
---------------------------------------
查看 Pods:        kubectl get pods
查看日志:         kubectl logs -l app=fe-demo
进入容器:         kubectl exec -it <pod-name> -- sh
扩容:            kubectl scale deployment/fe-demo-deployment --replicas=5
删除部署:         kubectl delete -f k8s/

EOF

# 询问是否立即启动端口转发
echo ""
read -p "是否立即启动端口转发？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    info "启动端口转发... (按 Ctrl+C 停止)"
    info "浏览器访问: http://localhost:8080"
    kubectl port-forward service/fe-demo-service 8080:80
fi
