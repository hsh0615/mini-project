# api/routing.py
from django.urls import path, re_path
from . import consumers

# 定義 WebSocket 路由，支援 matchId 作為動態路徑參數
websocket_urlpatterns = [
    re_path(r'ws/Chat/(?P<match_id>\w+)/$', consumers.ChatConsumer.as_asgi()),  # 動態路徑

]
