#!/bin/bash

# Kubernetes 应用访问脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 检查部署是否存在
if ! kubectl get deployment fe-demo-deployment &> /dev/null; then
    echo -e "${YELLOW}应用未部署！${NC}"
    echo "请先运行: ./deploy-k8s.sh"
    exit 1
fi

# 检查 Pod 状态
POD_STATUS=$(kubectl get pods -l app=fe-demo -o jsonpath='{.items[0].status.phase}' 2>/dev/null)

if [ "$POD_STATUS" != "Running" ]; then
    warn "Pod 还未就绪，当前状态: $POD_STATUS"
    info "等待 Pod 启动..."
    kubectl wait --for=condition=ready pod -l app=fe-demo --timeout=60s || {
        echo "Pod 启动超时，请检查状态:"
        kubectl get pods -l app=fe-demo
        exit 1
    }
fi

info "✓ Pod 运行正常"

# 显示 Pod 信息
echo ""
info "Pod 状态:"
kubectl get pods -l app=fe-demo

# 启动端口转发
echo ""
info "启动端口转发..."
info "浏览器访问: ${BLUE}http://localhost:8080${NC}"
info "按 ${YELLOW}Ctrl+C${NC} 停止"
echo ""

kubectl port-forward service/fe-demo-service 8080:80
