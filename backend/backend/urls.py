"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# 創建一個簡單的視圖函數來處理根路徑
def home(request):
    return HttpResponse("Hello, welcome to the MITLab Project API!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # 假設你的 API 有單獨的 `urls.py` 文件
    path('', home),  # 新增這行來處理根路徑
    
]
