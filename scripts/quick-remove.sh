#!/bin/bash

# 一键删除部署脚本

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${RED}⚠ 即将删除所有部署的资源${NC}"
echo ""
read -p "确认删除？(y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

echo "删除应用资源..."
kubectl delete -k k8s/ 2>/dev/null || echo "应用资源已删除或不存在"

echo ""
read -p "是否同时删除 Ingress Controller？(y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "删除 Ingress Controller..."
    kubectl delete namespace ingress-nginx 2>/dev/null || echo "Ingress Controller 已删除或不存在"
fi

echo ""
echo -e "${GREEN}✓ 清理完成！${NC}"
