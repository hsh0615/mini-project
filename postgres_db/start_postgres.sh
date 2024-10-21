#!/bin/bash

# 檢查 PostgreSQL 是否在運行
if pg_isready -q; then
    echo "PostgreSQL is already running."
else
    echo "Starting PostgreSQL..."
    service postgresql start  # 將此命令替換為你的系統啟動命令
fi

# 等待 PostgreSQL 完全啟動
sleep 5  # 等待幾秒鐘讓 PostgreSQL 完全啟動

# 檢查 PostgreSQL 是否已經成功啟動
if pg_isready -q; then
    echo "PostgreSQL started successfully."
else
    echo "Failed to start PostgreSQL."
    exit 1
fi
