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

from generation import views

urlpatterns = [
    path('full_state', views.full_state, name='full_state'),  # 全状态
    path('full_migration', views.full_migration, name='full_migration'),  # 全迁移
    path('path_list', views.path_list, name='path_list'),  # 路径列表
    path('generate_increase', views.generate_increase, name='generate_increase'),  # 递增值
    path('generate_decrease', views.generate_decrease, name='generate_decrease'),  # 递减值
    path('generate_random', views.generate_random, name='generate_random'),  # 随机值
    path('generate_boundary', views.generate_boundary, name='generate_boundary'),  # 边界值
    path('generate_mcdc', views.generate_mcdc, name='generate_mcdc'),  # MC/DC覆盖
]
