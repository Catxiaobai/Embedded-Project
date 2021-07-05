import base64
import json
import os
from json import dumps

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

import lwn_Graphic.combination
import lwn_Graphic.combination2
import lwn_Graphic.constructModel
import lwn_Graphic.constructModel2
from background.models import *
from entity.models import *
from lwn_Graphic import analysisXMI
from server import error_code


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
        filename = request_json['name']
        item_id = request_json['item']['id']
        filepath = './file/'
        analysisXMI.analysis(filepath, filename)
        filename = 'xmiModel.txt'
        save_model_to_db(filepath, filename, item_id)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def save_model_to_db(filepath, filename, item_id):
    list_xmi = []
    with open(filepath + filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').strip()
            list_xmi.append(line)
    # 清空Node和edge表
    Node.objects.all().delete()
    Edge.objects.all().delete()
    # 从txt中写入数据库里
    i = 0
    while i < len(list_xmi):
        state = {}
        transition = {}
        if list_xmi[i] == 'State:':
            for j in range(2):
                i = i + 1
                s = list_xmi[i].split('=', 1)
                state[s[0]] = s[-1]
            # print(state)
            Node(item_id=item_id, label=state['label'], name=state['name']).save()
        elif list_xmi[i] == 'Transition:':
            for j in range(6):
                i = i + 1
                t = list_xmi[i].split('=', 1)
                transition[t[0]] = t[-1]
            # print(transition)
            transition['src'] = Node.objects.filter(name=transition['src'])[0].to_dict()['id']
            transition['tgt'] = Node.objects.filter(name=transition['tgt'])[0].to_dict()['id']
            Edge(item_id=item_id, name=transition['name'],
                 src_id=transition['src'], tgt_id=transition['tgt'],
                 event=transition['event'], condition=transition['condition'],
                 action=transition['action']).save()
        i = i + 1


def modeling_from_db(request):
    request_jsons = json.loads(request.body)
    try:
        item_id = request_jsons['id']
        nodes = Node.objects.filter(item_id=item_id)
        edges = Edge.objects.filter(item_id=item_id)
        nodeData = [node.to_show() for node in nodes]
        edgeData = [edge.to_show() for edge in edges]
        # print(nodeData)
        # print(edgeData)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "nodeDataArray": nodeData, "linkDataArray": edgeData})


def save_model_to_xmi_model(request):
    request_jsons = json.loads(request.body)
    try:
        # print(request_jsons)
        filepath = './file/'
        filename = 'xmiModel.txt'
        nodeData = request_jsons['nodeDataArray']
        edgeData = request_jsons['linkDataArray']
        print(nodeData)
        print(edgeData)
        with open(filepath + filename, 'w', encoding='utf-8') as f:
            for node in nodeData:
                f.write("State:\n\tname=" + node['text'] + '\n\t' + "label=" + node['label'] + '\n')
            for edge in edgeData:
                f.write("Transition:\n\tname=" + edge['text'] + '\n\tsrc=' + edge['from']
                        + '\n\ttgt=' + edge['to'] + '\n\t' + 'event=' + edge['event'] + '\n\t' +
                        'condition=' + edge['condition'] + '\n\t' + 'action=' + edge['action'] + '\n')
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def save_model_to_txt(request):
    request_jsons = json.loads(request.body)
    try:
        # print(request_jsons)
        filepath = './file/'
        filename = 'newModel.txt'
        nodeData = request_jsons['nodeDataArray']
        edgeData = request_jsons['linkDataArray']
        print(nodeData)
        print(edgeData)
        with open(filepath + filename, 'w', encoding='utf-8') as f:
            for node in nodeData:
                f.write("State:\n\tname=" + node['text'] + '\n\t' + "label=" + node['label'] + '\n')
            for edge in edgeData:
                f.write("Transition:\n\tname=" + edge['text'] + '\n\tsrc=' + edge['from']
                        + '\n\ttgt=' + edge['to'] + '\n\t' + 'event=' + edge['event'] + '\n\t' +
                        'condition=' + edge['condition'] + '\n\t' + 'action=' + edge['action'] + '\n')
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def load_txt(request):
    request_jsons = json.loads(request.body)
    try:
        filepath = './file/'
        filename = 'newModel.txt'
        item_id = request_jsons['id']
        save_model_to_db(filepath, filename, item_id)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def import_model(request):
    request_jsons = json.loads(request.body)
    try:
        filepath = './file/'
        filename = request_jsons['name']
        item_id = request_jsons['item']['id']
        save_model_to_db(filepath, filename, item_id)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def node_edge_list(request):
    request_jsons = json.loads(request.body)
    try:
        item_id = request_jsons['id']
        nodes = Node.objects.filter(item_id=item_id)
        node_list = [n.to_dict() for n in nodes]
        edges = Edge.objects.filter(item_id=item_id)
        edge_list = [e.to_dict() for e in edges]
        print(node_list)
        print(edge_list)
        print(node_list + edge_list)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "result": node_list + edge_list})


def model_variable_options(request):
    request_jsons = json.loads(request.body)
    try:
        protocols = Protocol.objects.filter(item_id=request_jsons['id'])
        result = [p.to_dict() for p in protocols]
        options = []
        for protocol in result:
            print(protocol)
            option = {'value': protocol['subject_name'], 'label': protocol['subject_name'], 'children': []}
            print('option', option)

            config = eval(protocol['configuration'])
            result_conf = [Variable.objects.get(id=i).to_dict() for i in config]
            for i in result_conf:
                op = {}
                i.pop('id')
                i.pop('item')
                i.pop('describe')
                if i['value'] != 'None':
                    new_value = eval(i['value'])
                    i['value'] = new_value
                if i['type'] == 'CONSTANT':
                    i['type'] = 'constant'
                op['value'] = i['name']
                op['label'] = i['name']
                option['children'].append(op)
            options.append(option)
            print('options', options)
        print(options)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "options": options})


# 场景列表
def scenes_list(request):
    request_json = json.loads(request.body)
    try:
        scenes = Scenes.objects.filter(item_id=request_json['id'])
        result = [scene.to_dict() for scene in scenes]
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, "scenes_list": result})


def upload_static_model(request):
    myfile = request.FILES['file']
    fs = FileSystemStorage(location='file')
    if fs.exists(myfile.name):
        fs.delete(myfile.name)
    fs.save(myfile.name, myfile)
    desstr = myfile.name.split('.')[0]
    desstr += '.png'
    print(desstr)
    ''''''
    ENCODING = 'utf-8'
    file = open('file/' + desstr, 'rb')
    base64_data = base64.b64encode(file.read())
    base64_string = base64_data.decode(ENCODING)
    raw_data = {}
    raw_data["name"] = desstr
    raw_data["image_base64_string"] = base64_string
    json_data = dumps(raw_data)
    return JsonResponse({**error_code.CLACK_SUCCESS, "url": json_data})


def save_image(request):
    request_json = json.loads(request.body)
    try:
        Image(item_id=request_json['item']['id'],
              name=request_json['name'],
              src=request_json['src']).save()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


def load_image(request):
    request_json = json.loads(request.body)
    try:
        image = Image.objects.filter(item_id=request_json['item']['id'], name=request_json['name'])
        src = ''
        for i in image:
            src = i.to_dict()['src']
        print(src)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS, 'src': src})


# 删除场景
def delete_scenes(request):
    request_json = json.loads(request.body)
    try:
        # print(request_json)
        for i in range(len(request_json)):
            aim_id = request_json[i]['id']
            if not Scenes.objects.filter(id=aim_id).exists():
                return JsonResponse({**error_code.CLACK_NOT_EXISTS})
            Scenes.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 编辑场景
def edit_scenes(request):
    request_json = json.loads(request.body)
    try:
        new_describe = request_json['describe']
        new_element = request_json['element']
        new_content = request_json['content']
        aim_id = request_json['id']
        new_name = request_json['name']
        new_type = request_json['type']
        if not Scenes.objects.filter(id=aim_id).exists():
            return Scenes({**error_code.CLACK_NOT_EXISTS})
        Scenes.objects.filter(id=aim_id).update(name=new_name)
        Scenes.objects.filter(id=aim_id).update(type=new_type)
        Scenes.objects.filter(id=aim_id).update(describe=new_describe)
        Scenes.objects.filter(id=aim_id).update(element=new_element)
        Scenes.objects.filter(id=aim_id).update(content=new_content)
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


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
        # print('建模开始')
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




# 删除项目
def delete_item(request):
    request_json = json.loads(request.body)
    try:
        aim_id = request_json['id']
        Item.objects.get(id=aim_id).delete()
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 添加点和边
def add_node_link(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        get_type = request_jsons['type']
        get_item = request_jsons['item']
        get_addForm = request_jsons['addForm']
        file_path = './file/'

        new_node = {"label": get_addForm['node_label_show'],
                    "name": get_addForm['node_name']}
        new_link = {"name": get_addForm['link_name_show'],
                    "src": 'S' + str(get_addForm['source']),
                    "tgt": 'S' + str(get_addForm['target']),
                    "event": get_addForm['event'],
                    "condition": get_addForm['condition'],
                    "action": get_addForm['action']}
        # 修改result.txt
        if get_type == 'sub':
            file_name = 'result.txt'
        elif get_type == 'complex':
            file_name = 'result2.txt'
        with open(file_path + file_name, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        with open(file_path + file_name, 'w', encoding='utf-8') as f:
            for i in range(len(lines)):
                if lines[i] == 'Transition:' and lines[i - 3] == 'State:':
                    f.write('State:\n')
                    f.write('\tlabel=' + new_node['label'] + '\n')
                    f.write('\tname=' + new_node['name'] + '\n')
                if lines[i] != '':
                    print(lines[i])
                    f.write(lines[i] + '\n')
            f.write('Transition:\n'
                    + '\tname=' + new_link['name'] + '\n'
                    + '\tsrc=' + new_link['src'] + '\n'
                    + '\ttgt=' + new_link['tgt'] + '\n'
                    + '\tevent=' + new_link['event'] + '\n'
                    + '\tcondition=' + new_link['condition'] + '\n'
                    + '\taction=' + new_link['action'])
        # 修改resultModel.txt
        if get_type == 'sub':
            file_name = 'resultModel.txt'
        elif get_type == 'complex':
            file_name = 'resultModel2.txt'
        with open(file_path + file_name, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        with open(file_path + file_name, 'w', encoding='utf-8') as f:
            for i in range(len(lines)):
                if lines[i] == 'Transition:' and lines[i - 2] == 'State:':
                    f.write('State:\n')
                    f.write('\tname=' + new_node['label'] + '\n')
                if lines[i] != '':
                    print(lines[i])
                    f.write(lines[i] + '\n')
            if new_link['src'] == 'S0':
                new_link['src'] = 'START'
            f.write('Transition:\n'
                    + '\tname=' + new_link['name'] + '\n'
                    + '\tsrc=' + new_link['src'] + '\n'
                    + '\ttgt=' + new_link['tgt'] + '\n'
                    + '\tevent=' + new_link['event'] + '\n'
                    + '\tcondition=' + new_link['condition'] + '\n'
                    + '\taction=' + new_link['action'])
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 添加边
def add_link(request):
    request_jsons = json.loads(request.body)
    try:
        print(request_jsons)
        get_type = request_jsons['type']
        get_item = request_jsons['item']
        get_addForm = request_jsons['addForm']
        file_path = './file/'
        new_link = {"name": get_addForm['link_name_show'],
                    "src": 'S' + str(get_addForm['source']),
                    "tgt": 'S' + str(get_addForm['target']),
                    "event": get_addForm['event'],
                    "condition": get_addForm['condition'],
                    "action": get_addForm['action']}
        # 修改result.txt
        if get_type == 'sub':
            file_name = 'result.txt'
        elif get_type == 'complex':
            file_name = 'result2.txt'
        with open(file_path + file_name, 'a', encoding='utf-8') as f:
            f.write('Transition:\n'
                    + '\tname=' + new_link['name'] + '\n'
                    + '\tsrc=' + new_link['src'] + '\n'
                    + '\ttgt=' + new_link['tgt'] + '\n'
                    + '\tevent=' + new_link['event'] + '\n'
                    + '\tcondition=' + new_link['condition'] + '\n'
                    + '\taction=' + new_link['action'])

        # 修改resultModel.txt
        if get_type == 'sub':
            file_name = 'resultModel.txt'
        elif get_type == 'complex':
            file_name = 'resultModel2.txt'
        with open(file_path + file_name, 'a', encoding='utf-8') as f:
            if new_link['src'] == 'S0':
                new_link['src'] = 'START'
            if new_link['tgt'] == 'S0':
                new_link['tgt'] = 'START'
            f.write('Transition:\n'
                    + '\tname=' + new_link['name'] + '\n'
                    + '\tsrc=' + new_link['src'] + '\n'
                    + '\ttgt=' + new_link['tgt'] + '\n'
                    + '\tevent=' + new_link['event'] + '\n'
                    + '\tcondition=' + new_link['condition'] + '\n'
                    + '\taction=' + new_link['action'])
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 保存删除前模型
def save_delete(request):
    request_jsons = json.loads(request.body)
    try:
        get_item = request_jsons['item']
        get_type = request_jsons['type']
        file_path = './file/'
        if get_type == 'sub':
            file_name1 = 'result.txt'
            file_name2 = 'resultModel.txt'
        elif get_type == 'complex':
            file_name1 = 'result2.txt'
            file_name2 = 'resultModel2.txt'
        with open(file_path + 'deleteResult.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(file_path + file_name1, 'r', encoding='utf-8').read())
        with open(file_path + 'deleteResultModel.txt', 'wt+', encoding='utf-8') as f:
            f.write(open(file_path + file_name2, 'r', encoding='utf-8').read())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})


# 撤销删除边
def redo_delete(request):
    request_jsons = json.loads(request.body)
    try:
        get_item = request_jsons['item']
        get_type = request_jsons['type']
        file_path = './file/'
        if get_type == 'sub':
            file_name1 = 'result.txt'
            file_name2 = 'resultModel.txt'
        elif get_type == 'complex':
            file_name1 = 'result2.txt'
            file_name2 = 'resultModel2.txt'
        with open(file_path + file_name1, 'wt+', encoding='utf-8') as f:
            f.write(open(file_path + 'deleteResult.txt',
                         'r', encoding='utf-8').read())
        with open(file_path + file_name2, 'wt+', encoding='utf-8') as f:
            f.write(open(file_path + 'deleteResultModel.txt',
                         'r', encoding='utf-8').read())
    except Exception as e:
        return JsonResponse({**error_code.CLACK_UNEXPECTED_ERROR, "exception": e})
    return JsonResponse({**error_code.CLACK_SUCCESS})
