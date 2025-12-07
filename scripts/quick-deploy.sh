#!/bin/bash

# 一键部署脚本 - 包含完整的部署流程

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1"; exit 1; }
step() { echo -e "\n${BLUE}▶${NC} $1"; }

# 检查 Kubernetes 集群
step "检查 Kubernetes 集群"
kubectl cluster-info &> /dev/null || error "Kubernetes 集群未运行！请启动 Docker Desktop 中的 Kubernetes"
info "集群运行正常"

# 检查 Docker 镜像
step "检查 Docker 镜像"
if ! docker images fe-demo:latest --format "{{.Repository}}" | grep -q "fe-demo"; then
    warn "镜像不存在，开始构建..."
    docker build -f docker/Dockerfile -t fe-demo:latest . || error "镜像构建失败"
    info "镜像构建完成"
else
    info "镜像已存在"
fi

# 检查 Ingress Controller
step "检查 Ingress Controller"
if ! kubectl get deployment -n ingress-nginx ingress-nginx-controller &> /dev/null; then
    warn "Ingress Controller 未安装，开始安装..."
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
    info "等待 Ingress Controller 就绪..."
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=120s || warn "等待超时，请稍后手动检查"

    # 修改端口为 8898
    kubectl patch svc ingress-nginx-controller -n ingress-nginx --type='json' -p='[{"op": "replace", "path": "/spec/ports/0/port", "value": 8898}]'
    info "Ingress Controller 已安装（端口：8898）"
else
    info "Ingress Controller 已存在"
    # 确认端口是 8898
    current_port=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.spec.ports[0].port}')
    if [ "$current_port" != "8898" ]; then
        warn "端口不是 8898，正在修改..."
        kubectl patch svc ingress-nginx-controller -n ingress-nginx --type='json' -p='[{"op": "replace", "path": "/spec/ports/0/port", "value": 8898}]'
        info "端口已修改为 8898"
    else
        info "端口配置正确（8898）"
    fi
fi

# 使用 Kustomize 部署应用
step "部署应用"
kubectl apply -k k8s/
info "应用部署完成"

# 等待 Pod 就绪
step "等待 Pod 就绪"
kubectl wait --for=condition=ready pod -l app=fe-demo --timeout=60s || warn "等待超时"

# 显示部署状态
step "部署状态"
echo ""
kubectl get deployments fe-demo-deployment
echo ""
kubectl get pods -l app=fe-demo
echo ""
kubectl get svc fe-demo-service
echo ""
kubectl get ingress

# 访问说明
echo ""
echo -e "${GREEN}🎉 部署成功！${NC}"
echo ""
echo "访问地址："
echo -e "  ${BLUE}http://localhost:8898${NC}"
echo ""
echo "常用命令："
echo "  查看 Pods:    kubectl get pods"
echo "  查看日志:     kubectl logs -l app=fe-demo"
echo "  删除部署:     kubectl delete -k k8s/"
echo "  重新部署:     $0"
echo ""
