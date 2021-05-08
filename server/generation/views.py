import json

from django.http import JsonResponse

from entity.models import Paths
from server import error_code


# 全状态
def full_state(request):
    request_json = json.loads(request.body)
    aim_item_id = request_json['item']['id']
    try:
        # print(request_json)

        # 先在input填入type=1
        filename = 'input.txt'
        path = './efsmGA/files/'
        with open(path + filename, 'w+', encoding='utf-8') as f:
            content = {"type": 1}
            json.dump(content, f)

        # 读取输入文件，运行ga程序
        # with open(path + filename, 'r', encoding='utf-8') as f:
        #     content = f.read()
        #     print(content)
        #     os.system('py -2 ' + './efsmGA/ga.py')

        # 读取生成的output.txt
        filename = 'json格式样例2.txt'
        with open(path + filename, 'r', encoding='utf-8') as f:
            results = f.read()
        results_json = json.loads(results)
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
    return JsonResponse({**error_code.CLACK_SUCCESS, "results": results})


# 全迁移
def full_migration(request):
    request_json = json.loads(request.body)
    aim_item_id = request_json['item']['id']
    try:
        # print(request_json)

        # 先在input填入type=1
        filename = 'input.txt'
        path = './efsmGA/files/'
        with open(path + filename, 'w+', encoding='utf-8') as f:
            content = {"type": 2}
            json.dump(content, f)

        # 读取输入文件，运行ga程序
        # with open(path + filename, 'r', encoding='utf-8') as f:
        #     content = f.read()
        #     print(content)
        #     os.system('py -2 ' + './efsmGA/ga.py')

        # 读取生成的output.txt
        filename = 'json格式样例2.txt'
        with open(path + filename, 'r', encoding='utf-8') as f:
            results = f.read()
        results_json = json.loads(results)
        print(results_json)

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
    return JsonResponse({**error_code.CLACK_SUCCESS, "results": results})


# 路径列表
def path_list(request):
    try:
        paths = Paths.objects.all()
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
    print(request_json['info'])
    try:
        pass
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
