"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from background import views

urlpatterns = [
    path('item_list', views.item_list, name='item_list'),  # 项目列表
    path('login', views.login, name='login'),  # 登录
    path('personnel_list', views.personnel_list, name='personnel_list'),  # 人员列表
    path('add_item', views.add_item, name='add_item'),  # 添加项目
    path('user_item', views.user_item, name='user_item'),  # 用户所属项目
]
