#!/bin/bash

# 查看所有 kubectl port-forward 进程

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===========================================${NC}"
echo -e "${BLUE}   Kubectl Port-Forward 状态查看${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# 查找所有 kubectl port-forward 进程
KUBECTL_PROCS=$(ps aux | grep "kubectl port-forward" | grep -v grep)

if [ -z "$KUBECTL_PROCS" ]; then
    echo -e "${YELLOW}没有运行中的 kubectl port-forward 进程${NC}"
    echo ""
    exit 0
fi

# 统计数量
COUNT=$(echo "$KUBECTL_PROCS" | wc -l | tr -d ' ')
echo -e "${GREEN}找到 $COUNT 个 kubectl port-forward 进程:${NC}"
echo ""

# 显示详细信息
echo -e "${BLUE}PID\tPORT\tCOMMAND${NC}"
echo "-------------------------------------------"

echo "$KUBECTL_PROCS" | while read line; do
    # 提取 PID
    PID=$(echo $line | awk '{print $2}')

    # 提取命令
    CMD=$(echo $line | grep -o "kubectl port-forward.*" | head -1)

    # 尝试提取端口
    PORT=$(echo $CMD | grep -o "[0-9]*:80" | cut -d: -f1 | head -1)

    if [ -z "$PORT" ]; then
        PORT="?"
    fi

    echo -e "${GREEN}$PID${NC}\t${YELLOW}$PORT${NC}\t$CMD"
done

echo ""
echo -e "${BLUE}===========================================${NC}"

# 显示端口监听详情
echo ""
echo -e "${BLUE}端口监听详情:${NC}"
echo "-------------------------------------------"
lsof -nP -iTCP -sTCP:LISTEN | grep kubectl | awk '{printf "%-8s %-15s %s\n", $2, $9, $1}'

echo ""
echo -e "${BLUE}===========================================${NC}"

# 提示如何停止
echo ""
echo -e "${YELLOW}如何停止 port-forward:${NC}"
echo "  方法 1: kill <PID>"
echo "  方法 2: 使用停止脚本"
echo "  方法 3: pkill -f 'kubectl port-forward'"
echo ""

# 显示当前转发的资源
echo -e "${BLUE}当前转发的资源:${NC}"
echo "-------------------------------------------"
echo "$KUBECTL_PROCS" | grep -o "service/[^ ]*\|pod/[^ ]*\|deployment/[^ ]*" | sort | uniq | while read resource; do
    echo -e "  ${GREEN}✓${NC} $resource"
done

echo ""
