#!/bin/bash

# 停止所有 kubectl port-forward 进程

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===========================================${NC}"
echo -e "${BLUE}   停止 Kubectl Port-Forward${NC}"
echo -e "${BLUE}===========================================${NC}"
echo ""

# 查找所有 kubectl port-forward 进程
PIDS=$(ps aux | grep "kubectl port-forward" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo -e "${YELLOW}没有运行中的 kubectl port-forward 进程${NC}"
    echo ""
    exit 0
fi

# 统计数量
COUNT=$(echo "$PIDS" | wc -l | tr -d ' ')
echo -e "${YELLOW}找到 $COUNT 个进程，准备停止...${NC}"
echo ""

# 显示将要停止的进程
ps aux | grep "kubectl port-forward" | grep -v grep | while read line; do
    PID=$(echo $line | awk '{print $2}')
    CMD=$(echo $line | grep -o "kubectl port-forward.*" | head -1)
    echo -e "${YELLOW}停止:${NC} PID $PID - $CMD"
done

echo ""
read -p "确认停止这些进程？(y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 停止所有进程
    echo "$PIDS" | while read pid; do
        if kill $pid 2>/dev/null; then
            echo -e "${GREEN}✓${NC} 已停止进程 $pid"
        else
            echo -e "${RED}✗${NC} 无法停止进程 $pid"
        fi
    done

    echo ""
    echo -e "${GREEN}完成！${NC}"

    # 验证
    sleep 1
    REMAINING=$(ps aux | grep "kubectl port-forward" | grep -v grep | wc -l | tr -d ' ')
    if [ "$REMAINING" -eq 0 ]; then
        echo -e "${GREEN}所有 port-forward 已停止${NC}"
    else
        echo -e "${YELLOW}仍有 $REMAINING 个进程运行${NC}"
        echo "如果需要强制停止，运行: pkill -9 -f 'kubectl port-forward'"
    fi
else
    echo -e "${YELLOW}已取消${NC}"
fi

echo ""
