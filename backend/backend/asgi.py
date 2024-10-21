# backend/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from api.routing import websocket_urlpatterns

# 根據環境變數來選擇 settings
environment = os.getenv('DJANGO_ENV', 'local')  # 默認為本地開發環境

if environment == 'docker':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.docker')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
