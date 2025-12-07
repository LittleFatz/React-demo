# Docker 容器状态查看完全指南

## 基础命令

### 1. docker ps - 查看运行中的容器

```bash
docker ps
```

**显示**: 只显示正在运行的容器

**输出示例**:
```
CONTAINER ID   IMAGE          COMMAND        CREATED        STATUS        PORTS                  NAMES
9d5a2a3084b3   fe-demo:latest "/docker-..."   5 minutes ago  Up 5 minutes  0.0.0.0:8080->80/tcp   my-app
```

### 2. docker ps -a - 查看所有容器 ⭐

```bash
docker ps -a
```

**显示**: 所有容器（运行中 + 已停止 + 已暂停）

**最常用的命令！**

## 🔍 输出字段详解

```
CONTAINER ID   IMAGE          COMMAND              CREATED         STATUS                    PORTS                  NAMES
9d5a2a3084b3   fe-demo:latest "/docker-entrypo..." 10 minutes ago  Up 10 minutes            0.0.0.0:8080->80/tcp   my-app
abc123def456   nginx:alpine   "nginx -g 'daem..."  1 hour ago      Exited (0) 30 minutes ago                        web-server
```

| 字段 | 说明 | 示例 |
|------|------|------|
| CONTAINER ID | 容器唯一标识符（短格式） | 9d5a2a3084b3 |
| IMAGE | 使用的镜像 | fe-demo:latest |
| COMMAND | 容器启动时执行的命令 | "/docker-entrypoint..." |
| CREATED | 容器创建时间 | 10 minutes ago |
| STATUS | 容器当前状态 | Up 10 minutes |
| PORTS | 端口映射 | 0.0.0.0:8080->80/tcp |
| NAMES | 容器名称 | my-app |

## 📊 常用选项

### 只显示容器 ID

```bash
# 运行中的容器 ID
docker ps -q

# 所有容器 ID
docker ps -aq

# 示例输出:
9d5a2a3084b3
abc123def456
```

**用途**: 批量操作
```bash
# 停止所有容器
docker stop $(docker ps -q)

# 删除所有停止的容器
docker rm $(docker ps -aq -f status=exited)
```

### 显示最近创建的 N 个容器

```bash
# 最近 3 个容器
docker ps -a -n 3

# 最近 5 个容器
docker ps -a -n 5
```

### 显示最新创建的容器

```bash
docker ps -l
```

### 不截断输出

```bash
# 默认会截断长内容
docker ps

# 显示完整信息（不截断）
docker ps --no-trunc
```

**对比**:
```bash
# 默认（截断）
COMMAND
"/docker-entrypoint...."

# --no-trunc（完整）
COMMAND
"/docker-entrypoint.sh nginx -g 'daemon off;'"
```

### 显示文件大小

```bash
docker ps -s

# 或
docker ps --size
```

**输出**:
```
CONTAINER ID   IMAGE    SIZE
9d5a2a3084b3   fe-demo  2B (virtual 53.6MB)
              │         │           │
              │         │           └─ 虚拟大小（镜像+容器层）
              │         └─ 容器可写层大小
              └─ 容器ID
```

## 🎯 过滤选项 (--filter)

### 按状态过滤

```bash
# 运行中的容器
docker ps -a --filter "status=running"

# 已停止的容器
docker ps -a --filter "status=exited"

# 暂停的容器
docker ps -a --filter "status=paused"

# 正在重启的容器
docker ps -a --filter "status=restarting"
```

**所有状态值**:
- `created` - 已创建但未启动
- `restarting` - 正在重启
- `running` - 运行中
- `removing` - 正在删除
- `paused` - 已暂停
- `exited` - 已退出
- `dead` - 死亡状态

### 按名称过滤

```bash
# 精确匹配
docker ps -a --filter "name=my-app"

# 模糊匹配（包含 "app"）
docker ps -a --filter "name=app"
```

### 按镜像过滤

```bash
# 使用特定镜像的容器
docker ps -a --filter "ancestor=fe-demo:latest"

# 使用 nginx 镜像的所有容器
docker ps -a --filter "ancestor=nginx"
```

### 按退出码过滤

```bash
# 退出码为 0（正常退出）
docker ps -a --filter "exited=0"

# 退出码为 1（异常退出）
docker ps -a --filter "exited=1"

# 退出码为 137（被 kill 杀死）
docker ps -a --filter "exited=137"
```

**常见退出码**:
| 退出码 | 含义 |
|--------|------|
| 0 | 正常退出 ✅ |
| 1 | 应用错误 ❌ |
| 125 | Docker 守护进程错误 |
| 126 | 命令无法执行 |
| 127 | 命令未找到 |
| 137 | SIGKILL (被杀死) |
| 143 | SIGTERM (正常终止信号) |
| 255 | 退出码超出范围 |

### 按创建时间过滤

```bash
# 在某个容器之前创建的
docker ps --filter "before=my-app"

# 在某个容器之后创建的
docker ps --filter "since=my-app"
```

### 按标签过滤

```bash
# 有特定标签的容器
docker ps --filter "label=env=production"

# 有标签键的容器（无论值是什么）
docker ps --filter "label=env"
```

### 按网络过滤

```bash
# 连接到特定网络的容器
docker ps --filter "network=my-network"
```

### 按数据卷过滤

```bash
# 挂载了特定卷的容器
docker ps --filter "volume=my-volume"
```

### 组合多个过滤条件

```bash
# 运行中的 nginx 容器
docker ps --filter "status=running" --filter "ancestor=nginx"

# 已停止且退出码为 0 的容器
docker ps -a --filter "status=exited" --filter "exited=0"

# 名称包含 "app" 且运行中的容器
docker ps --filter "name=app" --filter "status=running"
```

## 🎨 格式化输出 (--format)

### 自定义列

```bash
# 只显示 ID 和名称
docker ps --format "{{.ID}}\t{{.Names}}"

# 输出:
9d5a2a3084b3    my-app
abc123def456    web-server
```

### 使用表格格式

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"

# 输出:
CONTAINER ID   NAMES        STATUS
9d5a2a3084b3   my-app       Up 10 minutes
abc123def456   web-server   Exited (0) 5 minutes ago
```

### 可用的格式化占位符

| 占位符 | 说明 |
|--------|------|
| `.ID` | 容器 ID |
| `.Image` | 镜像名称 |
| `.Command` | 启动命令 |
| `.CreatedAt` | 创建时间（时间戳） |
| `.RunningFor` | 运行时长 |
| `.Ports` | 端口映射 |
| `.Status` | 状态 |
| `.Size` | 文件大小 |
| `.Names` | 容器名称 |
| `.Labels` | 所有标签 |
| `.Label` | 特定标签值 |
| `.Mounts` | 挂载的卷 |
| `.Networks` | 网络设置 |

### 实用格式化示例

#### 简洁列表
```bash
docker ps --format "{{.Names}}: {{.Status}}"

# 输出:
my-app: Up 10 minutes
web-server: Exited (0) 5 minutes ago
```

#### 详细表格
```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

# 输出:
NAMES        IMAGE            STATUS           PORTS
my-app       fe-demo:latest   Up 10 minutes    0.0.0.0:8080->80/tcp
web-server   nginx:alpine     Up 5 minutes     0.0.0.0:80->80/tcp
```

#### JSON 格式
```bash
docker ps --format "{{json .}}"

# 输出:
{"Command":"\"/docker-entrypoint.sh nginx -g 'daemon off;'\"","CreatedAt":"2025-12-01 13:30:05 +0800 CST",...}
```

#### 美化 JSON
```bash
docker ps --format "{{json .}}" | jq
```

## 🔄 实时监控

### watch 命令持续监控

```bash
# 每 2 秒刷新一次
watch -n 2 docker ps

# 每 1 秒刷新，高亮变化
watch -n 1 -d docker ps
```

### 结合 grep 过滤

```bash
# 只看名称包含 "app" 的容器
docker ps | grep app

# 只看运行中的 nginx 容器
docker ps | grep nginx
```

## 📊 统计信息

### 查看资源使用情况

```bash
# 实时查看所有容器资源使用
docker stats

# 只显示一次（不持续）
docker stats --no-stream

# 只看特定容器
docker stats my-app

# 自定义格式
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

**输出**:
```
CONTAINER ID   NAME     CPU %   MEM USAGE / LIMIT   MEM %   NET I/O       BLOCK I/O
9d5a2a3084b3   my-app   0.01%   2.5MiB / 1.944GiB   0.13%   1.2kB / 0B    0B / 0B
```

### 查看容器详细信息

```bash
# 查看完整配置
docker inspect my-app

# 只看特定信息（使用 Go 模板）
docker inspect --format '{{.State.Status}}' my-app

# 查看 IP 地址
docker inspect --format '{{.NetworkSettings.IPAddress}}' my-app

# 查看环境变量
docker inspect --format '{{.Config.Env}}' my-app
```

## 💡 实用命令组合

### 清理停止的容器

```bash
# 查看所有停止的容器
docker ps -a --filter "status=exited"

# 删除所有停止的容器
docker rm $(docker ps -aq --filter "status=exited")

# 或使用 prune（推荐）
docker container prune
```

### 找出占用端口的容器

```bash
# 找出使用 8080 端口的容器
docker ps --filter "publish=8080"

# 或使用 grep
docker ps | grep 8080
```

### 批量停止容器

```bash
# 停止所有运行中的容器
docker stop $(docker ps -q)

# 停止特定镜像的所有容器
docker stop $(docker ps -q --filter "ancestor=nginx")

# 停止名称匹配的容器
docker stop $(docker ps -q --filter "name=app")
```

### 批量删除容器

```bash
# 删除所有容器（危险！）
docker rm -f $(docker ps -aq)

# 删除已停止的容器
docker rm $(docker ps -aq --filter "status=exited")

# 删除特定镜像的所有容器
docker rm $(docker ps -aq --filter "ancestor=old-image")
```

### 导出容器列表

```bash
# 导出为 CSV
docker ps -a --format "{{.ID}},{{.Names}},{{.Status}},{{.Image}}" > containers.csv

# 导出为 JSON
docker ps -a --format "{{json .}}" > containers.json

# 导出为表格文件
docker ps -a > containers.txt
```

## 🐛 故障排查

### 查看容器日志

```bash
# 查看容器日志
docker logs my-app

# 实时查看日志（类似 tail -f）
docker logs -f my-app

# 查看最后 100 行
docker logs --tail 100 my-app

# 显示时间戳
docker logs -t my-app

# 查看最近 5 分钟的日志
docker logs --since 5m my-app
```

### 检查容器为什么退出

```bash
# 查看退出码
docker ps -a --filter "name=my-app" --format "{{.Status}}"

# 查看完整日志
docker logs my-app

# 查看容器事件
docker events --filter "container=my-app"

# 查看详细信息
docker inspect my-app | grep -A 10 "State"
```

### 找出资源占用高的容器

```bash
# 按 CPU 使用率排序
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}" | sort -k 2 -hr

# 按内存使用排序
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" | sort -k 2 -hr
```

## 📝 快速参考

### 基础命令
```bash
docker ps                    # 运行中的容器
docker ps -a                 # 所有容器 ⭐
docker ps -q                 # 只显示 ID
docker ps -l                 # 最新容器
docker ps -n 5               # 最近 5 个
docker ps --no-trunc         # 完整信息
docker ps -s                 # 显示大小
```

### 过滤命令
```bash
docker ps --filter "status=running"      # 运行中
docker ps --filter "status=exited"       # 已停止
docker ps --filter "name=my-app"         # 按名称
docker ps --filter "ancestor=nginx"      # 按镜像
docker ps --filter "exited=0"            # 按退出码
```

### 格式化命令
```bash
docker ps --format "{{.Names}}: {{.Status}}"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
docker ps --format "{{json .}}" | jq
```

### 统计命令
```bash
docker stats                 # 实时资源监控
docker stats --no-stream     # 单次统计
docker inspect my-app        # 详细信息
```

## 🎯 最佳实践

1. **定期清理**: 使用 `docker ps -a` 查看并清理不需要的容器
2. **使用过滤**: 在容器多时，使用 `--filter` 快速定位
3. **自定义格式**: 创建别名保存常用格式
4. **监控资源**: 定期运行 `docker stats` 检查资源使用
5. **查看日志**: 容器异常时先查看 `docker logs`

## 💡 Shell 别名推荐

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
# 查看所有容器
alias dps='docker ps -a'

# 查看运行中的容器
alias dpsr='docker ps'

# 格式化查看
alias dpsf='docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'

# 查看容器资源
alias dstats='docker stats --no-stream'

# 清理停止的容器
alias dprune='docker container prune'
```

使用：
```bash
dps        # 快速查看所有容器
dpsr       # 快速查看运行中的容器
dpsf       # 格式化查看
```

## 总结

### 最常用的命令

```bash
# 这两个命令解决 90% 的需求
docker ps              # 看运行中的
docker ps -a           # 看所有的 ⭐⭐⭐

# 加上这些更完美
docker ps -a --filter "status=exited"     # 看停止的
docker ps --format "table {{.Names}}\t{{.Status}}"  # 简洁查看
docker stats --no-stream                   # 资源使用
```

记住：`docker ps -a` 是你的好朋友！🚀
