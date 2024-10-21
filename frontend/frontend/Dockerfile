# 使用官方的 Node.js 基本映像檔
FROM node:16-alpine

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝專案依賴
RUN npm install

# 複製專案文件
COPY . .

# 暴露應用程式在3000端口
EXPOSE 3000

# 啟動應用程式
CMD ["npm", "start"]
