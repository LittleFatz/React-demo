#!/bin/bash

# FE-DEMO Kubernetes 部署脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置变量
IMAGE_NAME="fe-demo"
IMAGE_TAG="latest"
NAMESPACE="default"
REGISTRY=""  # 如果使用远程仓库,在这里设置,例如: docker.io/username

# 打印信息
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

# 检查必要的工具
check_requirements() {
    info "检查必要工具..."

    if ! command -v docker &> /dev/null; then
        error "Docker 未安装,请先安装 Docker"
    fi

    if ! command -v kubectl &> /dev/null; then
        error "kubectl 未安装,请先安装 kubectl"
    fi

    info "✓ 所有必要工具已安装"
}

# 构建 Docker 镜像
build_image() {
    info "开始构建 Docker 镜像..."

    if [ -n "$REGISTRY" ]; then
        FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
    else
        FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"
    fi

    docker build -t "$FULL_IMAGE_NAME" . || error "镜像构建失败"

    info "✓ 镜像构建成功: $FULL_IMAGE_NAME"
}

# 推送镜像到仓库
push_image() {
    if [ -n "$REGISTRY" ]; then
        info "推送镜像到仓库..."
        docker push "$FULL_IMAGE_NAME" || error "镜像推送失败"
        info "✓ 镜像推送成功"
    else
        warn "未配置镜像仓库,跳过推送步骤"
        warn "如果部署到远程集群,请配置 REGISTRY 变量"
    fi
}

# 部署到 Kubernetes
deploy_to_k8s() {
    info "开始部署到 Kubernetes..."

    # 如果配置了镜像仓库,更新 deployment.yaml
    if [ -n "$REGISTRY" ]; then
        info "更新 deployment 配置..."
        sed -i.bak "s|image:.*|image: $FULL_IMAGE_NAME|g" k8s/deployment.yaml
    fi

    # 应用配置
    kubectl apply -f k8s/deployment.yaml -n "$NAMESPACE" || error "Deployment 部署失败"
    kubectl apply -f k8s/service.yaml -n "$NAMESPACE" || error "Service 部署失败"
    kubectl apply -f k8s/ingress.yaml -n "$NAMESPACE" || error "Ingress 部署失败"

    # 恢复原配置文件(如果有备份)
    if [ -f "k8s/deployment.yaml.bak" ]; then
        mv k8s/deployment.yaml.bak k8s/deployment.yaml
    fi

    info "✓ 部署完成"
}

# 等待部署完成
wait_for_deployment() {
    info "等待部署就绪..."
    kubectl rollout status deployment/fe-demo-deployment -n "$NAMESPACE" --timeout=5m || error "部署超时"
    info "✓ 部署已就绪"
}

# 显示部署状态
show_status() {
    info "部署状态:"
    echo ""
    kubectl get pods -l app=fe-demo -n "$NAMESPACE"
    echo ""
    kubectl get svc fe-demo-service -n "$NAMESPACE"
    echo ""
    kubectl get ingress fe-demo-ingress -n "$NAMESPACE"
}

# 主函数
main() {
    info "开始 FE-DEMO Kubernetes 部署流程"
    echo ""

    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --registry)
                REGISTRY="$2"
                shift 2
                ;;
            --tag)
                IMAGE_TAG="$2"
                shift 2
                ;;
            --namespace)
                NAMESPACE="$2"
                shift 2
                ;;
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            --help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --registry REGISTRY    镜像仓库地址 (例如: docker.io/username)"
                echo "  --tag TAG             镜像标签 (默认: latest)"
                echo "  --namespace NAMESPACE Kubernetes 命名空间 (默认: default)"
                echo "  --skip-build          跳过镜像构建步骤"
                echo "  --help                显示帮助信息"
                exit 0
                ;;
            *)
                error "未知参数: $1 (使用 --help 查看帮助)"
                ;;
        esac
    done

    check_requirements

    if [ "$SKIP_BUILD" != true ]; then
        build_image
        push_image
    else
        info "跳过镜像构建步骤"
    fi

    deploy_to_k8s
    wait_for_deployment
    show_status

    echo ""
    info "🎉 部署成功完成!"
    info "使用以下命令查看应用状态:"
    echo "  kubectl get pods -l app=fe-demo -n $NAMESPACE"
    echo "  kubectl logs -l app=fe-demo -n $NAMESPACE"
}

# 执行主函数
main "$@"
