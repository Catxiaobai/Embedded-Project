import json
import os
import random

import lwn_Graphic.combination
import lwn_Graphic.combination2
import lwn_Graphic.constructModel
import lwn_Graphic.constructModel2
import dsp.main

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from server import error_code
from entity.models import Personnel, Item, Scenes
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


# 人员列表
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


# 上传文件
def upload_file(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage(location='file')
    if fs.exists(myfile.name):
        fs.delete(myfile.name)
    fs.save(myfile.name, myfile)
    return JsonResponse({**error_code.CLACK_SUCCESS})


def import_xmi(request):
    request_json = json.loads(request.body)
    try:
        pass
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 场景列表
def scenes_list(request):
    request_json = json.loads(request.body)
    try:
        scenes = Scenes.objects.filter(item_id=request_json['id'])
        result = [scene.to_dict() for scene in scenes]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "scenes_list": result})


def import_scenes(request):
    request_json = json.loads(request.body)
    filename = request_json['name']
    new_type = request_json['type']
    new_item = request_json['item']
    print(request_json)
    try:
        with open('./file/' + filename, 'r', encoding='utf-8') as f:
            original_file = f.read()
            lines = original_file.splitlines()
        index = 0
        while index < len(lines):
            if '0' <= lines[index][0] <= '9':
                index += 1
                new_content = ""
                new_name = ""
                new_describe = ""
                new_element = ""
                if lines[index] == "element:":
                    index += 1
                    new_element = lines[index]
                    index += 1
                if lines[index] == "name:":
                    index += 1
                    new_name = lines[index]
                    index += 1
                if lines[index] == "describe:":
                    index += 1
                    new_describe = lines[index]
                    index += 1
                if lines[index] == "content:":
                    index += 1
                while index < len(lines) and (lines[index][0] < '0' or lines[index][0] > '9'):
                    new_content = new_content + lines[index] + '\n'
                    index += 1
                scenes = Scenes(item_id=new_item['id'],
                                element=new_element,
                                content=new_content,
                                type=new_type,
                                name=new_name,
                                describe=new_describe)
                scenes.save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def scenes_modeling(request):
    request_jsons = json.loads(request.body)
    print(request_jsons)
    try:
        print('建模开始')
        scenes = Scenes.objects.filter(
            item_id=request_jsons['item']['id'], type=request_jsons['type'], element=request_jsons['element'])
        if request_jsons['type'] == 'sub':
            filename = 'Trace.txt'
        elif request_jsons['type'] == 'complex':
            filename = 'Trace2.txt'
        f = open('./file/' + filename, 'w', encoding='utf-8')
        for s in scenes:
            # print(s.to_dict())
            ch = s.to_dict()
            f.write('Trace:' + '\n')
            f.write(ch['content'])
            f.write('\n')
        f.close()
        if request_jsons['type'] == 'sub':
            lwn_Graphic.constructModel.main()
            print('建模')
            # lwn_Graphic.combination.combination()
            filepath = './file/'
            with open(filepath + 'resultSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'result.txt',
                             'r', encoding='utf-8').read())
            with open(filepath + 'resultModelSaveCreate.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'resultModel.txt',
                             'r', encoding='utf-8').read())
        elif request_jsons['type'] == 'complex':
            lwn_Graphic.constructModel2.main()
            # lwn_Graphic.combination2.combination()
            filepath = './file/'
            with open(filepath + 'resultSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'result2.txt',
                             'r', encoding='utf-8').read())
            with open(filepath + 'resultModelSaveCreate2.txt', 'wt+', encoding='utf-8') as f:
                f.write(open(filepath + 'resultModel2.txt',
                             'r', encoding='utf-8').read())
        # Models.objects.all().delete()
        # scenes2 = Scenes.objects.filter(item_id=request_jsons['item']['id'])
        # for s in scenes2:
        #     model_name = s.to_dict['']
        #     models = Models(name=s.to_dict[''])
        #     Models.save(models)
        print('建模结束')
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def deliver_model_data(request):
    request_jsons = json.loads(request.body)
    if request_jsons['type'] == 'sub':
        file_name = './file/result.txt'
    elif request_jsons['type'] == 'complex':
        file_name = './file/result2.txt'
    lines = open(file_name, 'r', encoding='UTF-8').readlines()
    index_line = 0
    data_node = []
    data_edge = []
    test_id = 1
    while index_line < len(lines):
        if lines[index_line].strip() == "State:":
            index_line += 1
            node_num0 = lines[index_line].strip().split('=')[1]
            node_num = int(node_num0[1:])
            node_label = lines[index_line].strip().split('=')[1]
            if node_label == 'S0':
                node_label = 'START'
            index_line += 1
            node_name = lines[index_line].strip().split('=', 1)[1]
            # data.append({"data": {"id": node_name, "label": node_name, "category": node_category.get(node_name, 2)}})
            # data.append({"data": {"id": node_name, "label": node_label,"name":node_name}})
            data_node.append(
                {"id": node_num, "text": node_label, 'name': node_name})
        if lines[index_line].strip() == "Transition:":
            index_line += 1
            name = lines[index_line].strip().split('=', 1)[1]
            index_line += 1
            src0 = lines[index_line].strip().split('=', 1)[1]
            src = int(src0[1:])
            index_line += 1
            tgt0 = lines[index_line].strip().split('=', 1)[1]
            tgt = int(tgt0[1:])
            index_line += 1
            event = lines[index_line].strip().split('=', 1)
            event = event[1] if len(event) > 1 else ""
            index_line += 1
            cond = lines[index_line].strip().split('=', 1)
            cond = cond[1] if len(cond) > 1 else ""
            index_line += 1
            action = lines[index_line].strip().split('=', 1)
            action = action[1] if len(action) > 1 else ""
            edge = {"id": test_id, "from": src, "to": tgt, "text": name, "event": event, "cond": cond,
                    "action": action, "color": "black"}
            # print(edge)
            test_id += 1
            data_edge.append(edge)

        index_line += 1
    # print(data_edge)
    return JsonResponse({**error_code.CLACK_SUCCESS, "data_node": data_node, "data_edge": data_edge})


# 保存编辑前的模型样子
def save_model2(request):
    filepath = './file/'
    with open(filepath + 'resultSave2.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'result2.txt', 'r', encoding='utf-8').read())
    with open(filepath + 'resultModelSave2.txt', 'wt+', encoding='utf-8') as f:
        f.write(open(filepath + 'resultModel2.txt', 'r', encoding='utf-8').read())
    return JsonResponse({**error_code.CLACK_SUCCESS})


def dsp_test(request):
    dsp.main.start()
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 删除项目
def delete_item(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        Item.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})

