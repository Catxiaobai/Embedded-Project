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

