#!/bin/bash

# 確認當前處於 frontend 資料夾中
cd ..

# 檢查 Node.js 和 npm 是否已安裝
if ! command -v npm &> /dev/null
then
    echo "npm not found, please install Node.js and npm first."
    exit
fi

if ! command -v node &> /dev/null
then
    echo "Node.js not found, please install Node.js first."
    exit
fi

# 安裝前端依賴
echo "Installing frontend dependencies..."
npm install

# 啟動 React 開發伺服器
echo "Starting frontend server..."
npm start

# 保持腳本運行
wait
