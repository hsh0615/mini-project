# api/routing.py
from django.urls import path
from .consumers import MatchConsumer

# 定義 WebSocket 路由
websocket_urlpatterns = [
    path('ws/match/', MatchConsumer.as_asgi()),  # 路徑與 MatchConsumer 綁定
]
