import json
import os
import re

from django.http import JsonResponse

from entity.models import Paths, Protocol
from generation.models import PathsData
from lwn_Graphic import script
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


# 数据列表
def data_list(request):
    request_json = json.loads(request.body)
    print(request_json)
    try:
        path_data = PathsData.objects.filter(paths_id=request_json['id'], name=request_json['name'])
        result = [p.to_dict() for p in path_data]
        print(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "data_list": result})


# 生成递增值
def generate_increase(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 3
        old_input['path'] = eval(request_json['path'])
        old_input['amount'] = request_json['amount']
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '递增值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成递减值
def generate_decrease(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 4
        old_input['path'] = eval(request_json['path'])
        old_input['amount'] = request_json['amount']
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '递减值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成随机值
def generate_random(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 1
        old_input['path'] = eval(request_json['path'])
        old_input['time'] = request_json['time']
        old_input['amount'] = request_json['amount']
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '随机值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成边界值
def generate_boundary(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 2
        old_input['path'] = eval(request_json['path'])
        old_input['precision'] = request_json['precision']
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '边界值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成MC/DC数据
def generate_mcdc(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 5
        old_input['path'] = eval(request_json['path'])
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = 'MC/DC'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成条件覆盖数据
def generate_condition(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 6
        old_input['path'] = eval(request_json['path'])
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '条件覆盖'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


def xmi_modeling(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        # constructModel.main()
        print('建模')
        filepath = './file/'
        with open(filepath + 'resultSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(filepath + 'result2.txt',
                         'r', encoding='utf-8').read())
        with open(filepath + 'resultModelSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(filepath + 'resultModel2.txt',
                         'r', encoding='utf-8').read())

    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def scenes_modeling(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        # constructModel.main()
        # print('建模')
        filepath = './file/'
        with open(filepath + 'result2.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(filepath + 'model.txt',
                         'r', encoding='utf-8').read())
        with open(filepath + 'resultSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(filepath + 'result2.txt',
                         'r', encoding='utf-8').read())
        with open(filepath + 'resultModelSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(filepath + 'resultModel2.txt',
                         'r', encoding='utf-8').read())

    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 脚本生成
def generate_script(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        result = []
        filepath = './efsmGA/files/'
        filename = 'efsm_atm.txt'
        for key in request_jsons:
            regular = re.compile(r"T[0-9]+")
            if regular.match(key):
                print(key, request_jsons[key])
                result.append(script.main(key, request_jsons[key], filepath + filename))
        print(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": result})


# 新建协议
def add_protocol(request):
    request_json = json.loads(request.body)
    try:
        new_subject_name = request_json['subject_name']
        new_date = request_json['date']
        new_version = request_json['version']
        new_bus_type = request_json['bus_type']
        new_communication_method = request_json['communication_method']
        new_refresh_cycle = request_json['refresh_cycle']
        new_frame_header = request_json['frame_header']
        new_frame_tail = request_json['frame_tail']
        new_check_method = request_json['check_method']
        new_item_id = request_json['item_id']
        if Protocol.objects.filter(item_id=new_item_id, bus_type=new_bus_type):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_protocol = Protocol(
            subject_name=new_subject_name,
            date=new_date,
            version=new_version,
            bus_type=new_bus_type,
            communication_method=new_communication_method,
            refresh_cycle=new_refresh_cycle,
            frame_header=new_frame_header,
            frame_tail=new_frame_tail,
            check_method=new_check_method,
            item_id=new_item_id)
        new_protocol.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 协议列表
def protocol_list(request):
    request_json = json.loads(request.body)
    try:
        protocols = Protocol.objects.filter(item_id=request_json['id'])
        result = [p.to_dict() for p in protocols]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "protocol_list": result})


# 编辑协议
def edit_protocol(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        new_subject_name = request_json['subject_name']
        new_date = request_json['date']
        new_version = request_json['version']
        new_bus_type = request_json['bus_type']
        new_communication_method = request_json['communication_method']
        new_refresh_cycle = request_json['refresh_cycle']
        new_frame_header = request_json['frame_header']
        new_frame_tail = request_json['frame_tail']
        new_check_method = request_json['check_method']
        if not Protocol.objects.filter(id=aim_id).exists():
            return Protocol({**error_code.CLACK_NOT_EXISTS})
        Protocol.objects.filter(id=aim_id).update(subject_name=new_subject_name)
        Protocol.objects.filter(id=aim_id).update(date=new_date)
        Protocol.objects.filter(id=aim_id).update(version=new_version)
        Protocol.objects.filter(id=aim_id).update(bus_type=new_bus_type)
        Protocol.objects.filter(id=aim_id).update(communication_method=new_communication_method)
        Protocol.objects.filter(id=aim_id).update(refresh_cycle=new_refresh_cycle)
        Protocol.objects.filter(id=aim_id).update(frame_header=new_frame_header)
        Protocol.objects.filter(id=aim_id).update(frame_tail=new_frame_tail)
        Protocol.objects.filter(id=aim_id).update(check_method=new_check_method)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除协议
def delete_protocol(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        Protocol.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除协议
def get_parameter(request):
    try:
        path = "./efsmGA/files/"
        filename = 'parameter.txt'
        parameter = read_txt(path, filename)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "parameter": parameter})


def test(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        result = script.main(request_jsons['pass'])
        print(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": result})
