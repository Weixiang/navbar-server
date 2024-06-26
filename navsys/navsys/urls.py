"""
URL configuration for navsys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from rest_framework.authtoken import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from navsysMain.views import (
    index, 
    PublishMessageView, 
    CallDeviceAPIView, 
    CallItemsAPIView, 
    GetItemByRFIDAPIView, 
    EncryptAPIView,
    DecryptAPIView,
    query_item_by_rfid,
    crypt,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='project_home'),  # 项目主页
    path('rfid/', query_item_by_rfid, name='query_item_by_rfid'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('crypt/', crypt, name='encrypt_decrypt'),

    path('favicon.ico', RedirectView.as_view(url=r'static/icon/favicon.ico')),

    path('api/publish', PublishMessageView.as_view(), name='publish_message'),
    path('api/calldevice', CallDeviceAPIView.as_view(), name='call_device_api'),
    path('api/callitems', CallItemsAPIView.as_view(), name='call_items_api'),
    path('api/getitems', GetItemByRFIDAPIView.as_view(), name='get_item_by_rfid'),
    path('api/token', views.obtain_auth_token, name='token_obtain_pair'),
    path('api/encrypt', EncryptAPIView.as_view(), name='encrypt_payload'),
    path('api/decrypt', DecryptAPIView.as_view(), name='decrypt_payload'),
]