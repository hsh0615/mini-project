# backend/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack  # 支持用户认证
from django.core.asgi import get_asgi_application
from api.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 支持 HTTP 请求
    "websocket": AuthMiddlewareStack(  # 支持 WebSocket 用户认证
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
