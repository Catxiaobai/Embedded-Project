import json
import os

from django.http import JsonResponse

from entity.models import Paths
from server import error_code


# 从txt读取内容，返回json解析数据
def read_txt(path, filename):
    with open(path + filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content_json = json.loads(content)
    # print(content_json)
    return content_json


# 将json数据写入txt中
def write_txt(path, filename, content):
    with open(path + filename, 'w+', encoding='utf-8') as f:
        json.dump(content, f)


# 全状态
def full_state(request):
    request_json = json.loads(request.body)
    aim_item_id = request_json['item']['id']
    try:
        # 将input.txt文件的type改为1
        path = './efsmGA/files/'
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 1
        write_txt(path, filename, old_input)
        # 运行ga程序
        os.system('py -2 ' + './efsmGA/ga.py')
        # 读取生成的output.txt
        filename = 'output.txt'
        results_json = read_txt(path, filename)
        print(results_json)
        # 写入数据库中，先判断这个模型是否之前跑过，如果有就删，无直接加
        new_type = 'state'
        Paths.objects.filter(item_id=aim_item_id, type=new_type).delete()
        for key, value in results_json.items():
            if key != 'name':
                print(key, value)
                new_path = value
                new_paths = Paths(type=new_type, item_id=aim_item_id, path=new_path)
                new_paths.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "results": results_json})


# 全迁移
def full_migration(request):
    request_json = json.loads(request.body)
    aim_item_id = request_json['item']['id']
    try:
        # 将input.txt文件的type改为2
        path = './efsmGA/files/'
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 2
        write_txt(path, filename, old_input)
        # 读取输入文件，运行ga程序
        os.system('py -2 ' + './efsmGA/ga.py')
        # 读取生成的output.txt
        filename = 'output.txt'
        results_json = read_txt(path, filename)
        # 写入数据库中，先判断这个模型是否之前跑过，如果有就删，无直接加
        new_type = 'migration'
        Paths.objects.filter(item_id=aim_item_id, type=new_type).delete()
        for key, value in results_json.items():
            if key != 'name':
                print(key, value)
                new_path = value
                new_paths = Paths(type=new_type, item_id=aim_item_id, path=new_path)
                new_paths.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "results": results_json})


# 路径列表
def path_list(request):
    request_json = json.loads(request.body)
    try:
        paths = Paths.objects.filter(item_id=request_json['id'])
        result = [p.to_dict() for p in paths]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": result})


# 生成递增值
def generate_increase(request):
    request_json = json.loads(request.body)
    print(request_json['info'])
    try:
        pass
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成递减值
def generate_decrease(request):
    request_json = json.loads(request.body)
    print(request_json['info'])
    try:
        pass
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成随机值
def generate_random(request):
    request_json = json.loads(request.body)
    print(request_json)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 1
        print('test', request_json['path'])
        # print('aa', request_json['path'])
        old_input['path'] = eval(request_json['path'])
        old_input['time'] = request_json['time']
        old_input['amount'] = request_json['amount']
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成边界值
def generate_boundary(request):
    request_json = json.loads(request.body)
    print(request_json['info'])
    try:
        pass
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成MC/DC数据
def generate_mcdc(request):
    request_json = json.loads(request.body)
    print(request_json['info'])
    try:
        pass
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})
