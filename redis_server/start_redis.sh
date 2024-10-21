#!/bin/bash

# 檢查 Redis 是否在運行
if redis-cli ping | grep -q "PONG"; then
    echo "Redis is already running."
else
    echo "Starting Redis..."
    service redis-server start  # 將此命令替換為你的系統啟動命令
fi

# 等待 Redis 完全啟動
sleep 3  # 等待幾秒鐘讓 Redis 完全啟動

# 檢查 Redis 是否已經成功啟動
if redis-cli ping | grep -q "PONG"; then
    echo "Redis started successfully."
else
    echo "Failed to start Redis."
    exit 1
fi
