# 使用官方的 Python 映像作為基礎
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝必需的編譯工具和依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libdbus-1-dev \
    libglib2.0-dev \
    libcairo2-dev \
    pkg-config \
    gobject-introspection \
    libgirepository1.0-dev \
    libsystemd-dev \
    && rm -rf /var/lib/apt/lists/*

# # 複製 requirements.txt 並安裝 Python 依賴
# COPY docker.txt ./
# 複製 requirements/docker.txt 並安裝 Python 依賴
COPY requirements/docker.txt ./docker.txt

# 安裝 virtualenv 工具來創建虛擬環境
RUN python -m venv /opt/venv

# 激活虛擬環境並更新 pip
RUN /opt/venv/bin/python -m pip install --upgrade pip

# # 安裝專案依賴到虛擬環境中
# RUN /opt/venv/bin/pip install --no-cache-dir -r requirements-docker.txt
# 安裝專案依賴到虛擬環境中
RUN /opt/venv/bin/pip install --no-cache-dir -r docker.txt

# 複製專案文件到容器中
COPY . .

# 暴露 Django 和 WebSocket 使用的端口
EXPOSE 8050 8080

# 設置默認環境變量以使用虛擬環境中的 Python
ENV PATH="/opt/venv/bin:$PATH"

# 啟動 Django 和 Daphne (WebSocket)
# CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && (python manage.py runserver 0.0.0.0:8050 &) && daphne -b 0.0.0.0 -p 8080"]
# 使用 Daphne 來處理 WebSocket server
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && daphne -b 0.0.0.0 -p 8080 backend.asgi:application & python manage.py runserver 0.0.0.0:8050"]
