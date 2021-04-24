import json
import os
import random

from django.http import JsonResponse
from server import error_code
from entity.models import Personnel, Item
from background.models import ItemPerson


# 登录权限
def login(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        users = Personnel.objects.filter(
            account=request_jsons['account'], password=request_jsons['password'])
        print(Personnel.objects.all())
        user = [item.to_dict() for item in users]
        print(user)
        if len(user) == 0:
            return JsonResponse({**error_code.CLACK_USER_LOGIN_FAILED})
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "user": user[0]['account'], 'user_info': user[0]})


# 模型列表
def personnel_list(request):
    try:
        persons = Personnel.objects.all()
        result = [p.to_dict() for p in persons]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "personnel_list": result})


# 查询全部项目
def item_list(request):
    try:
        items = Item.objects.all()
        result = [item.to_dict() for item in items]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "item_list": result})


# 新建项目
def add_item(request):
    request_json = json.loads(request.body)
    try:
        new_name = request_json['name']
        new_software = request_json['software']
        new_team = request_json['team']
        new_level = request_json['level']
        new_path = request_json['path']
        if Item.objects.filter(name=new_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_item = Item(name=new_name,
                        software=new_software,
                        team=new_team,
                        level=new_level,
                        path=new_path)
        # 创建文件夹
        if os.path.isdir('./' + new_path + '/' + new_name):
            return JsonResponse({**error_code.CLACK_DIR_EXISTS})
        else:
            os.makedirs('./' + new_path + '/' + new_name)
            os.makedirs('./' + new_path + '/' + new_name + '/' + 'modelfiles')
            new_item.save()
        print(new_item.to_dict())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "item": new_item.to_dict()})


def user_item(request):
    request_jsons = json.loads(request.body)
    try:
        user_id = request_jsons['id']
        items = ItemPerson.objects.filter(personnel_id=user_id)
        result = [item.to_dict() for item in items]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "item_list": result})
