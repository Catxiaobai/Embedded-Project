import json
import os
import random

from django.http import JsonResponse
from server import error_code
from entity.models import Personnel


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
