#!/bin/bash
echo "Starting databases..."
# 啟動 PostgreSQL
cd postgres_db
./start_postgres.sh

# 啟動 Redis
cd ../redis_server
./start_redis.sh

# 進入 backend 的 shell 資料夾並啟動後端
echo "Starting backend..."
cd ../backend/shell
./create_django_app.sh &  # 背景啟動後端

# 返回到主目錄並進入 frontend 的 shell 資料夾啟動前端
cd ../../frontend/frontend/shell
echo "Starting frontend..."
./create_frontend_app.sh &  # 背景啟動前端

# 保持腳本運行
wait
