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
    path('data_list', views.data_list, name='data_list'),  # 数据列表
    path('generate_increase', views.generate_increase, name='generate_increase'),  # 递增值
    path('generate_decrease', views.generate_decrease, name='generate_decrease'),  # 递减值
    path('generate_random', views.generate_random, name='generate_random'),  # 随机值
    path('generate_boundary', views.generate_boundary, name='generate_boundary'),  # 边界值
    path('generate_mcdc', views.generate_mcdc, name='generate_mcdc'),  # MC/DC覆盖
    path('generate_condition', views.generate_condition, name='generate_condition'),  # 条件覆盖
    path('xmi_modeling', views.xmi_modeling, name='xmi_modeling'),  # xmi建模
    path('scenes_modeling', views.scenes_modeling, name='scenes_modeling'),  # 建模
    path('generate_script', views.generate_script, name='generate_script'),  # 脚本生成
    path('add_protocol', views.add_protocol, name='add_protocol'),  # 添加通信协议
    path('protocol_list', views.protocol_list, name='protocol_list'),  # 通信协议列表
    path('edit_protocol', views.edit_protocol, name='edit_protocol'),  # 编辑通信协议
    path('delete_protocol', views.delete_protocol, name='delete_protocol'),  # 删除通信协议
    path('commit_protocol', views.commit_protocol, name='commit_protocol'),  # 确定协议
    path('get_parameter', views.get_parameter, name='get_parameter'),  # 获取参数
    path('add_variable', views.add_variable, name='add_variable'),  # 添加变量
    path('variable_list', views.variable_list, name='variable_list'),  # 变量列表
    path('delete_variable', views.delete_variable, name='delete_variable'),  # 删除变量
    path('test_data_list', views.test_data_list, name='test_data_list'),  # 全部测试数据
    path('save_data', views.save_data, name='save_data'),  # 保存测试数据
    path('test', views.test, name='test'),  # 测试
]
