from django.db import models


# Create your models here.


# 人员
class Personnel(models.Model):
    name = models.TextField(default='')
    age = models.IntegerField(default=0, blank=True)
    gender = models.TextField(default='', blank=True)
    account = models.TextField(default='', unique=True)
    password = models.TextField(default='')
    authority = models.IntegerField(default='')
    team = models.TextField(default='', blank=True)

    def to_dict(self):
        if self.authority == 1:
            level = '普通成员'
        elif self.authority == 2:
            level = '项目管理员'
        elif self.authority == 3:
            level = '系统管理员'
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'account': self.account,
            'password': self.password,
            'authority': self.authority,
            'level': level,
            'team': self.team
        }


# 项目
class Item(models.Model):
    name = models.TextField(default='', unique=True)
    software = models.TextField(default='')
    team = models.TextField(default='')
    level = models.TextField(default='')
    path = models.TextField(default='')
    describe = models.TextField(default='', blank=True)

    # item_date = models.DateTimeField(default='')
    # item_leader = models.ForeignKey(Personnel, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'software': self.software,
            'team': self.team,
            'level': self.level,
            'path': self.path,
            'describe': self.describe
        }


# 场景
class Scenes(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    element = models.TextField(default='')
    content = models.TextField(default='')
    type = models.TextField(default='')
    name = models.TextField(default='')
    describe = models.TextField(default='')

    def to_dict(self):
        type2 = ''
        if self.type == 'sub':
            type2 = '子场景'
        elif self.type == 'complex':
            type2 = '综合场景'
        return {
            'id': self.id,
            'name': self.name,
            'element': self.element,
            'type': self.type,
            'type2': type2,
            'describe': self.describe,
            'content': self.content,
            'item': self.item.id,
            'model_name': self.name + '的状态图'
        }

    def reset_pk(self):
        self.id = None


# 场景
class Paths(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.TextField(default='')
    path = models.TextField(default='')

    def to_dict(self):
        type2 = ''
        if self.type == 'state':
            type2 = '全状态'
        elif self.type == 'migration':
            type2 = '全迁移'
        return {
            'id': self.id,
            'type': self.type,
            'type2': type2,
            'item': self.item.id,
            'path': self.path
        }


# 脚本
class Protocol(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    subject_name = models.TextField(default='')
    date = models.TextField(default='')
    version = models.TextField(default='')
    type = models.TextField(default='')
    communication_method = models.TextField(default='')
    configuration = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.id,
            'subject_name': self.subject_name,
            'date': self.date,
            'version': self.version,
            'type': self.type,
            'communication_method': self.communication_method,
            'configuration': self.configuration,
        }


# 变量
class Variable(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.TextField(default='')
    describe = models.TextField(default='')
    type = models.TextField(default='')
    upper_bound = models.TextField(default='')
    lower_bound = models.TextField(default='')
    value = models.TextField(default='')
    length = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.id,
            'name': self.name,
            'describe': self.describe,
            'type': self.type,
            'upper_bound': self.upper_bound,
            'lower_bound': self.lower_bound,
            'value': self.value,
            'length': self.length,
        }


# 测试数据
class TestData(models.Model):
    paths = models.ForeignKey(Paths, on_delete=models.CASCADE)
    type = models.TextField(default='')
    function = models.TextField(default='')
    data = models.TextField(default='')
    TF = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'path_id': self.paths.id,
            'path': self.paths.path,
            'type': self.type,
            'function': self.function,
            'data': self.data,
            'TF': self.TF
        }
