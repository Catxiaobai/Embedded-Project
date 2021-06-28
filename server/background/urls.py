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
    path('upload_file', views.upload_file, name='upload_file'),  # 上传文件
    path('import_xmi', views.import_xmi, name='import_xmi'),  # 导入xmi文件
    path('scenes_list', views.scenes_list, name='scenes_list'),  # 场景列表
    path('delete_scenes', views.delete_scenes, name='delete_scenes'),  # 删除场景
    path('edit_scenes', views.edit_scenes, name='edit_scenes'),  # 编辑场景
    path('import_scenes', views.import_scenes, name='import_scenes'),  # 导入场景
    path('scenes_modeling', views.scenes_modeling, name='scenes_modeling'),  # 场景建模
    path('deliver_model_data', views.deliver_model_data, name='deliver_model_data'),  # 传递模型的场景信息
    path('save_model2', views.save_model2, name='save_model2'),  # 保存模型原本的样子
    path('dsp_test', views.dsp_test, name='dsp_test'),
    path('delete_item', views.delete_item, name='delete_item'),  # 删除项目
    path('add_node_link', views.add_node_link, name='add_node_link'),  # 模型动态加点
    path('add_link', views.add_link, name='add_link'),  # 模型动态加边
    path('save_delete', views.save_delete, name='save_delete'),  # 保存删除前模型
    path('redo_delete', views.redo_delete, name='redo_delete'),  # 撤销删除边
    path('modeling_from_db', views.modeling_from_db, name='modeling_from_db'),  # 从数据库建模
    path('save_model_to_xmi_model', views.save_model_to_xmi_model, name='save_model_to_xmi_model'),
    path('load_txt', views.load_txt, name='load_txt'),
    path('save_model_to_txt', views.save_model_to_txt, name='save_model_to_txt'),
    path('import_model', views.import_model, name='import_model'),
    path('node_edge_list', views.node_edge_list, name='node_edge_list'),
    path('model_variable_options', views.model_variable_options, name='model_variable_options'),
    path('upload_static_model', views.upload_static_model, name='upload_static_model'),
    path('save_image', views.save_image, name='save_image'),
    path('load_image', views.load_image, name='load_image'),
]
