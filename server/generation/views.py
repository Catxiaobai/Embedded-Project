import json
import os
import re
import shutil

from django.http import JsonResponse

from entity.models import *
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


# 将output.txt内容修改成符合格式的数据
def edit_txt(path, filename):
    content = read_txt(path, filename)
    print(content)
    if content['name'] == '随机测试' or content['name'] == '接口异常':
        for key in content:
            if key != 'name':
                for k in content[key]:
                    content[key][k] = str(content[key][k])
        print(content)
    elif content['name'] == 'MC/DC测试' or content['name'] == '全条件测试':
        for key in content:
            if key != 'name':
                temp = []
                for k in content[key]:
                    print(content[key][k])
                    temp.append(str(content[key][k]))
                content[key] = temp
        print(content)
    else:
        for key in content:
            if key != 'name':
                for i in range(len(content[key])):
                    content[key][i] = str(content[key][i])
    write_txt(path, filename, content)


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
        with open(path + 'efsm_atm.txt', 'wt+', encoding='utf-8') as f:
            f.write(open('./file/' + 'newModel.txt',
                         'r', encoding='utf-8').read())
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
        with open(path + 'efsm_atm.txt', 'w', encoding='utf-8') as f:
            f.write(open('./file/' + 'newModel.txt',
                         'r', encoding='utf-8').read())
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
        new_name = request_json['name']
        path_data = PathsData.objects.filter(paths_id=request_json['id'], name=new_name)
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
        edit_txt(path, filename)
        result = read_txt(path, filename)
        # print('request_json', request_json)
        # print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '递增值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
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
        edit_txt(path, filename)
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
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
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
        edit_txt(path, filename)
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
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成时序
def generate_time(request):
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
        edit_txt(path, filename)
        result = read_txt(path, filename)
        print('request_json', request_json)
        print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '时序约束'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
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
        edit_txt(path, filename)
        result = read_txt(path, filename)
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '边界值'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
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
        edit_txt(path, filename)
        result = read_txt(path, filename)
        # print('request_json', request_json)
        # print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = 'MC/DC'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
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
        edit_txt(path, filename)
        result = read_txt(path, filename)
        # print('request_json', request_json)
        # print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '条件覆盖'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


# 生成接口异常数据
def generate_wrong(request):
    request_json = json.loads(request.body)
    try:
        # 修改输入信息
        path = "./efsmGA/files/"
        filename = 'input.txt'
        old_input = read_txt(path, filename)
        old_input['type'] = 7
        old_input['path'] = eval(request_json['path'])
        write_txt(path, filename, old_input)
        # 运行data程序
        os.system('py -2 ' + './efsmGA/data_generation.py')
        # 读取output.txt信息
        filename = 'output.txt'
        edit_txt(path, filename)
        result = read_txt(path, filename)
        # print('request_json', request_json)
        # print('result', str(result))
        # 判断这条path这种方法name下有没有生成data，有就delete，无则save
        aim_path_id = request_json['id']
        new_type2 = request_json['type2']
        new_name = '接口异常'
        new_data = result
        PathsData.objects.filter(paths_id=aim_path_id, name=new_name).delete()
        new_paths_data = PathsData(paths_id=aim_path_id, type2=new_type2, name=new_name, data=new_data)
        new_paths_data.save()
        # 将PathsData数据表中的数据存储到TestData表中
        save_test_data_to_db(new_paths_data.to_dict())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "path_list": request_json})


def save_test_data_to_db(data):
    print('data', data)
    # 先判断是否有数据生成，有就删了
    TestData.objects.filter(paths_id=data['path_id'], function=data['name'], type=data['type2']).delete()
    # TF标签
    tf = ''
    # data
    if data['name'] == '边界值' or data['name'] == '递增值' or data['name'] == '递减值':
        T = {}
        maxLen = 0
        for key in data['data']:
            regular = re.compile(r"T[0-9]+")
            if regular.match(key):
                T[key] = data['data'][key]
                maxLen = max(len(data['data'][key]), maxLen)
        for i in range(maxLen):
            new_data = []
            for key in T:
                if i < len(T[key]):
                    new_data.append(T[key][i])
                else:
                    new_data.append('')
            TestData(paths_id=data['path_id'],
                     type=data['type2'],
                     function=data['name'],
                     TF=tf,
                     data=new_data).save()
    elif data['name'] == '条件覆盖' or data['name'] == 'MC/DC':
        for key in data['data']:
            if key != 'name':
                tf = key
                new_data = data['data'][key]
                TestData(paths_id=data['path_id'],
                         type=data['type2'],
                         function=data['name'],
                         TF=tf,
                         data=new_data).save()
    elif data['name'] == '接口异常':
        state = ['正常', '帧头异常', '帧尾异常', '校验和异常']
        for i in range(len(state)):
            tf = state[i]
            new_data = []
            for key in data['data']:
                if key != 'name':
                    new_data.append(data['data'][key][state[i]])
            TestData(paths_id=data['path_id'],
                     type=data['type2'],
                     function=data['name'],
                     TF=tf,
                     data=new_data).save()
    elif data['name'] == '随机值' or data['name'] == '时序约束':
        for key in data['data']:
            new_data = []
            if key != 'name':
                for i in data['data'][key]:
                    new_data.append(data['data'][key][i])
                TestData(paths_id=data['path_id'],
                         type=data['type2'],
                         function=data['name'],
                         TF=tf,
                         data=new_data).save()


def save_data(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        aim_path_id = request_jsons[0]['path_id']
        new_function = request_jsons[0]['name']
        new_type = request_jsons[0]['type2']
        # 先判断是否有数据生成，有就删了
        TestData.objects.filter(paths_id=aim_path_id, function=new_function).delete()
        for request_json in request_jsons:
            # print(request_json)
            new_data = []
            new_TF = request_json['TF']
            for key in request_json:
                regular = re.compile(r"T[0-9]+")
                if regular.match(key):
                    # print(key, request_json[key])
                    new_data.append(request_json[key])
            # print(str(new_data))
            new_test_data = TestData(paths_id=aim_path_id,
                                     function=new_function,
                                     type=new_type,
                                     data=new_data,
                                     TF=new_TF)
            new_test_data.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


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


# 脚本生成
def generate_script_all(request):
    request_jsons = json.loads(request.body)
    # print(request_jsons)
    try:
        filepath = './efsmGA/files/'
        filename = 'efsm_atm.txt'
        dir_path = './modelfiles/' + request_jsons['item']['name']
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)
        for i in range(len(request_jsons['data'])):
            result = []
            path = eval(request_jsons['data'][i]['path'])
            data = eval(request_jsons['data'][i]['data'])
            # print(path)
            # print(data)
            for j in range(min(len(path), len(data))):
                result.append(script.main(path[j], data[j], filepath + filename))
            # print(i, result)
            with open(dir_path+'/script_'+str(i), 'w', encoding='utf-8') as f:
                for r in result:
                    f.write(r+'\n')
            # for key in request_jsons:
        #     regular = re.compile(r"T[0-9]+")
        #     if regular.match(key):
        #         print(key, request_jsons[key])
        #         result.append(script.main(key, request_jsons[key], filepath + filename))
        # print(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 新建协议
def add_protocol(request):
    request_json = json.loads(request.body)
    try:
        new_subject_name = request_json['subject_name']
        new_date = request_json['date']
        new_version = request_json['version']
        new_type = request_json['type']
        new_communication_method = request_json['communication_method']
        new_item_id = request_json['item_id']
        if Protocol.objects.filter(item_id=new_item_id, subject_name=new_subject_name):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_protocol = Protocol(
            subject_name=new_subject_name,
            date=new_date,
            version=new_version,
            type=new_type,
            communication_method=new_communication_method,

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
        new_type = request_json['type']
        new_communication_method = request_json['communication_method']

        if not Protocol.objects.filter(id=aim_id).exists():
            return Protocol({**error_code.CLACK_NOT_EXISTS})
        Protocol.objects.filter(id=aim_id).update(subject_name=new_subject_name)
        Protocol.objects.filter(id=aim_id).update(date=new_date)
        Protocol.objects.filter(id=aim_id).update(version=new_version)
        Protocol.objects.filter(id=aim_id).update(type=new_type)
        Protocol.objects.filter(id=aim_id).update(communication_method=new_communication_method)

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


# 获取参数
def get_parameter(request):
    try:
        path = "./efsmGA/files/"
        filename = 'parameter.txt'
        parameter = read_txt(path, filename)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "parameter": parameter})


# 变量列表
def variable_list(request):
    request_json = json.loads(request.body)
    try:
        variables = Variable.objects.filter(item_id=request_json['id'])
        result = [v.to_dict() for v in variables]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "variable_list": result})


# 添加变量
def add_variable(request):
    request_json = json.loads(request.body)
    try:
        print(request_json)
        new_name = request_json['name']
        new_describe = request_json['describe']
        new_type = request_json['type']
        new_upper_bound = request_json['upper_bound']
        new_lower_bound = request_json['lower_bound']
        new_value = request_json['value']
        new_length = request_json['length']
        new_item_id = request_json['item_id']
        if Variable.objects.filter(item_id=new_item_id, describe=new_describe):
            return JsonResponse({**error_code.CLACK_NAME_EXISTS})
        new_variable = Variable(
            name=new_name,
            describe=new_describe,
            type=new_type,
            value=new_value,
            length=new_length,
            upper_bound=new_upper_bound,
            lower_bound=new_lower_bound,
            item_id=new_item_id)
        new_variable.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除变量
def delete_variable(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        Variable.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 确定协议
def commit_protocol(request):
    request_jsons = json.loads(request.body)
    try:
        path = './efsmGA/files/'
        filename = 'format.txt'
        print(request_jsons)
        protocol = Protocol.objects.get(subject_name=request_jsons['protocol'], item_id=request_jsons['item_id'])
        print(protocol.to_dict())
        result = []
        if protocol.to_dict()['configuration'] != '':
            config = eval(protocol.to_dict()['configuration'])
            result = [Variable.objects.get(id=i).to_dict() for i in config]
            print(result)
        for i in result:
            i.pop('id')
            i.pop('item')
            i.pop('describe')
            if i['value'] != 'None':
                new_value = eval(i['value'])
                i['value'] = new_value
        print(result)
        write_txt(path, filename, result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def test_data_list(request):
    request_json = json.loads(request.body)
    print(request_json)
    try:
        test_data = TestData.objects.filter(paths__item_id=request_json['id'])
        result = [p.to_dict() for p in test_data]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "test_data_list": result})


def test(request):
    request_jsons = json.loads(request.body)
    try:
        path = './efsmGA/files/'
        filename = 'format.txt'
        # print(request_jsons[0].keys())
        for i in request_jsons:
            i.pop('id')
            i.pop('item')
            i.pop('describe')
            new_value = eval(i['value'])
            i['value'] = new_value
        write_txt(path, filename, request_jsons)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def current_protocol(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        protocol = Protocol.objects.get(subject_name=request_jsons['protocol'], item_id=request_jsons['item_id'])
        result = []
        if protocol.to_dict()['configuration'] != '':
            config = eval(protocol.to_dict()['configuration'])
            result = [Variable.objects.get(id=i).to_dict() for i in config]
            print(result)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": result})


def protocol_save(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        var = request_jsons['variable']
        config = []
        for i in var:
            config.append(i['id'])
        Protocol.objects.filter(
            subject_name=request_jsons['protocol'],
            item_id=request_jsons['item_id']).update(configuration=str(config))
        protocols = Protocol.objects.filter(item_id=request_jsons['item_id'])
        result = [p.to_dict() for p in protocols]
        print(result)
        results = {}
        for protocol in result:
            print(protocol)
            config = eval(protocol['configuration'])
            result_conf = [Variable.objects.get(id=i).to_dict() for i in config]
            for i in result_conf:
                i.pop('id')
                i.pop('item')
                i.pop('describe')
                if i['value'] != 'None':
                    new_value = eval(i['value'])
                    i['value'] = new_value
                if i['type'] == 'CONSTANT':
                    i['type'] = 'constant'
            results[protocol['subject_name']] = result_conf
        print(results)
        path = './efsmGA/files/'
        filename = 'format.txt'
        write_txt(path, filename, results)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})
