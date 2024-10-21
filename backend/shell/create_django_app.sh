#!/bin/bash

# 啟動腳本 - create_django_app.sh

cd ..
# 載入環境變數，並考慮空格和引號
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 創建虛擬環境（如果不存在）
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 啟動虛擬環境
source venv/bin/activate

# 安裝本地開發依賴
echo "Installing dependencies from requirements/local.txt..."
pip install -r requirements/local.txt

# 進行數據庫遷移
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# 啟動 Django 應用
echo "Starting Django server on port 8050..."
python manage.py runserver 0.0.0.0:8050 &  # 後台啟動

# 啟動 Daphne（WebSocket server）
echo "Starting WebSocket server on port 8080..."
daphne -b 0.0.0.0 -p 8080 backend.asgi:application

# 保持腳本運行
wait
