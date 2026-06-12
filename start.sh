#!/bin/bash

# =========================
# Trading Bot Launcher
# =========================

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "🚀 Starting Trading Bot..."

# 杀掉旧进程（安全重启）
pkill -f "main.py" || true
sleep 1

# 启动主程序
nohup python3 main.py > logs/run.log 2>&1 &

echo "✅ Trading Bot started"
echo "📄 Logs: logs/run.log"
