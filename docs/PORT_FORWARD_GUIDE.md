# Kubectl Port-Forward 管理指南

## 📋 什么是 Port-Forward？

`kubectl port-forward` 创建一个从本地到 Kubernetes 集群的**隧道**（不是规则），它是一个**运行的进程**。

```
你的电脑                           Kubernetes 集群
─────────                          ───────────────
localhost:8080 ──┐
                 │  kubectl
                 │  进程        ──────> Service/Pod (端口 80)
                 │  (隧道)
[::1]:8080 ──────┘
```

---

## 🔍 查看所有 Port-Forward

### 方法 1: 使用脚本（推荐）⭐

```bash
./check-port-forwards.sh
```

**输出示例**:
```
===========================================
   Kubectl Port-Forward 状态查看
===========================================

找到 1 个 kubectl port-forward 进程:

PID     PORT    COMMAND
-------------------------------------------
26355   8080    kubectl port-forward service/fe-demo-service 8080:80

端口监听详情:
-------------------------------------------
26355    127.0.0.1:8080  kubectl
26355    [::1]:8080      kubectl

当前转发的资源:
-------------------------------------------
  ✓ service/fe-demo-service
```

### 方法 2: 使用 lsof 查看端口

```bash
# 查看所有 kubectl 监听的端口
lsof -nP -iTCP -sTCP:LISTEN | grep kubectl

# 输出:
# kubectl 26355 user 8u IPv4 0x... TCP 127.0.0.1:8080 (LISTEN)
# kubectl 26355 user 9u IPv6 0x... TCP [::1]:8080 (LISTEN)
```

**字段说明**:
- `kubectl`: 进程名
- `26355`: 进程 ID (PID)
- `8u/9u`: 文件描述符
- `127.0.0.1:8080`: 本地 IPv4 监听地址和端口
- `[::1]:8080`: 本地 IPv6 监听地址和端口

### 方法 3: 使用 ps 查看进程

```bash
# 查看所有 kubectl port-forward 进程
ps aux | grep "kubectl port-forward" | grep -v grep

# 输出:
# user 26355 0.0 0.1 411899536 44928 ?? S 8:59PM 0:00.14 kubectl port-forward service/fe-demo-service 8080:80
```

**字段说明**:
- `26355`: 进程 ID (PID)
- `0.0`: CPU 使用率
- `0.1`: 内存使用率
- `S`: 进程状态 (S=sleeping/休眠)
- `kubectl port-forward...`: 完整命令

### 方法 4: 查看特定端口

```bash
# 查看某个端口是否被使用
lsof -ti:8080

# 输出进程 ID:
# 26355

# 查看端口详情
lsof -i:8080
```

### 方法 5: 查看所有监听的端口

```bash
# 查看所有监听的端口
lsof -nP -iTCP -sTCP:LISTEN

# 过滤 kubectl
lsof -nP -iTCP -sTCP:LISTEN | grep kubectl
```

---

## 🛠️ 管理 Port-Forward

### 启动 Port-Forward

#### 基本用法

```bash
# 转发 Service
kubectl port-forward service/fe-demo-service 8080:80

# 转发 Pod
kubectl port-forward pod/fe-demo-deployment-xxx 8080:80

# 转发 Deployment
kubectl port-forward deployment/fe-demo-deployment 8080:80
```

#### 后台运行

```bash
# 方法 1: 使用 nohup
nohup kubectl port-forward service/fe-demo-service 8080:80 > /dev/null 2>&1 &

# 方法 2: 使用脚本
./access-app.sh &

# 方法 3: 在新终端运行
# 打开新终端，运行 port-forward 命令
```

#### 转发多个端口

```bash
# 转发多个端口
kubectl port-forward service/my-service 8080:80 8443:443

# 随机本地端口
kubectl port-forward service/my-service :80
```

#### 指定监听地址

```bash
# 只监听本地
kubectl port-forward --address localhost service/fe-demo-service 8080:80

# 监听所有接口（危险，允许外部访问）
kubectl port-forward --address 0.0.0.0 service/fe-demo-service 8080:80
```

### 停止 Port-Forward

#### 方法 1: 使用脚本（推荐）⭐

```bash
./stop-port-forwards.sh
```

#### 方法 2: 使用 kill 命令

```bash
# 1. 找到进程 ID
lsof -ti:8080

# 2. 停止进程
kill <PID>

# 例如:
kill 26355

# 强制停止
kill -9 26355
```

#### 方法 3: 按端口停止

```bash
# 停止占用 8080 端口的进程
kill $(lsof -ti:8080)
```

#### 方法 4: 停止所有 kubectl port-forward

```bash
# 温和停止
pkill -f "kubectl port-forward"

# 强制停止
pkill -9 -f "kubectl port-forward"
```

#### 方法 5: 在运行的终端按 Ctrl+C

如果 port-forward 在前台运行：
```bash
# 按 Ctrl+C 停止
^C
```

---

## 📊 监控 Port-Forward

### 实时监控连接

```bash
# 查看日志（如果在前台运行）
kubectl port-forward service/fe-demo-service 8080:80

# 输出:
# Forwarding from 127.0.0.1:8080 -> 80
# Forwarding from [::1]:8080 -> 80
# Handling connection for 8080  ← 每次访问会显示
```

### 查看连接统计

```bash
# 查看网络连接
netstat -an | grep 8080

# macOS 使用:
lsof -i:8080 -sTCP:ESTABLISHED
```

### 测试连接

```bash
# 使用 curl 测试
curl http://localhost:8080

# 查看 HTTP 状态
curl -I http://localhost:8080

# 测试连接时间
curl -w "\nTime: %{time_total}s\n" http://localhost:8080
```

---

## 🐛 故障排查

### 问题 1: 端口已被占用

**现象**:
```
error: unable to listen on port 8080: Listeners failed to create with the following errors:
[unable to create listener: Error listen tcp4 127.0.0.1:8080: bind: address already in use]
```

**排查**:
```bash
# 查看占用端口的进程
lsof -i:8080

# 查看进程详情
ps aux | grep <PID>
```

**解决**:
```bash
# 方法 1: 停止占用端口的进程
kill $(lsof -ti:8080)

# 方法 2: 使用其他端口
kubectl port-forward service/fe-demo-service 8081:80

# 方法 3: 使用随机端口
kubectl port-forward service/fe-demo-service :80
```

### 问题 2: Port-Forward 断开

**现象**:
```
lost connection to pod
error: lost connection to pod
```

**原因**:
- Pod 重启
- 网络不稳定
- Kubernetes API Server 重启

**解决**:
```bash
# 重新建立连接
kubectl port-forward service/fe-demo-service 8080:80

# 或使用脚本自动重连
while true; do
  kubectl port-forward service/fe-demo-service 8080:80
  sleep 2
done
```

### 问题 3: 无法访问应用

**检查清单**:
```bash
# 1. 确认 port-forward 运行
ps aux | grep "kubectl port-forward"

# 2. 确认端口监听
lsof -i:8080

# 3. 测试连接
curl http://localhost:8080

# 4. 查看 Pod 状态
kubectl get pods

# 5. 查看 Pod 日志
kubectl logs <pod-name>
```

### 问题 4: 连接缓慢

**排查**:
```bash
# 测试响应时间
curl -w "Time: %{time_total}s\n" http://localhost:8080

# 查看 Pod 资源使用
kubectl top pod <pod-name>

# 查看 Pod 详情
kubectl describe pod <pod-name>
```

---

## 💡 最佳实践

### 1. 使用脚本管理

✅ **推荐**:
```bash
# 启动
./access-app.sh

# 查看
./check-port-forwards.sh

# 停止
./stop-port-forwards.sh
```

❌ **不推荐**:
```bash
# 手动记住端口和命令
kubectl port-forward service/... 8080:80
```

### 2. 使用一致的端口

```bash
# 为不同服务使用不同端口
8080: 前端应用
8081: 后端 API
8082: 数据库管理界面
3306: MySQL
5432: PostgreSQL
6379: Redis
```

### 3. 后台运行

```bash
# 生产环境建议后台运行
nohup kubectl port-forward service/fe-demo-service 8080:80 > /tmp/port-forward.log 2>&1 &

# 查看日志
tail -f /tmp/port-forward.log
```

### 4. 使用 Service 而不是 Pod

✅ **推荐** (使用 Service):
```bash
kubectl port-forward service/fe-demo-service 8080:80
```

❌ **不推荐** (使用 Pod):
```bash
kubectl port-forward pod/fe-demo-xxx 8080:80
# Pod 可能会重启，导致连接断开
```

### 5. 定期清理

```bash
# 定期检查
./check-port-forwards.sh

# 停止不需要的
./stop-port-forwards.sh
```

---

## 🆚 Port-Forward vs 其他访问方式

### Port-Forward vs NodePort

| 特性 | Port-Forward | NodePort |
|------|--------------|----------|
| 需要运行进程 | ✅ 是 | ❌ 否 |
| 持久化 | ❌ 重启失效 | ✅ 永久有效 |
| 端口范围 | 任意 | 30000-32767 |
| 适用场景 | 开发调试 | 测试环境 |
| 安全性 | ✅ 更安全 | ⚠️ 暴露端口 |

### Port-Forward vs LoadBalancer

| 特性 | Port-Forward | LoadBalancer |
|------|--------------|--------------|
| 云依赖 | ❌ 无 | ✅ 需要云环境 |
| 成本 | 免费 | 💰 收费 |
| 外部访问 | ❌ 本地 | ✅ 公网 |
| 适用场景 | 本地开发 | 生产环境 |

### Port-Forward vs Ingress

| 特性 | Port-Forward | Ingress |
|------|--------------|---------|
| 需要 Controller | ❌ 否 | ✅ 是 |
| 域名支持 | ❌ 否 | ✅ 是 |
| HTTPS | ❌ 否 | ✅ 是 |
| 多服务路由 | ❌ 否 | ✅ 是 |
| 适用场景 | 单一服务调试 | 生产环境 |

---

## 📝 快速参考

### 常用命令

```bash
# 查看所有 port-forward
./check-port-forwards.sh

# 启动 port-forward
kubectl port-forward service/fe-demo-service 8080:80

# 后台启动
./access-app.sh &

# 停止 port-forward
./stop-port-forwards.sh

# 查看端口占用
lsof -i:8080

# 停止特定端口
kill $(lsof -ti:8080)

# 测试连接
curl http://localhost:8080
```

### 一键命令

```bash
# 查看
alias kpf-list='ps aux | grep "kubectl port-forward" | grep -v grep'

# 停止所有
alias kpf-stop='pkill -f "kubectl port-forward"'

# 查看端口
alias port-check='lsof -nP -iTCP -sTCP:LISTEN | grep kubectl'
```

---

## 🎯 总结

### Port-Forward 不是"规则"，而是"进程"

```
❌ 错误理解: 配置了一条转发规则
✅ 正确理解: 运行了一个转发进程

类比:
Port-Forward 像一个邮递员（进程），不断在两个地址之间传递信件
规则（如 iptables）像一个路标，永久标记路线
```

### 核心要点

1. ✅ Port-Forward 是运行的进程
2. ✅ 使用 `ps` 或 `lsof` 查看
3. ✅ 使用 `kill` 停止
4. ✅ 重启电脑或终端关闭会失效
5. ✅ 适合开发调试，不适合生产

### 推荐工作流

```bash
# 1. 查看当前状态
./check-port-forwards.sh

# 2. 启动需要的转发
./access-app.sh

# 3. 开发/测试

# 4. 完成后清理
./stop-port-forwards.sh
```

---

**记住**: 每次需要访问应用，都要确保 port-forward 进程在运行！🚀
