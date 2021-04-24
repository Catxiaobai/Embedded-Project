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


# 项目表
class Item(models.Model):
    item_name = models.TextField(default='', unique=True)
    item_content = models.TextField(default='')
    item_describe = models.TextField(default='')

    def to_dict(self):
        return {
            'invalid_id': self.id,
            'item_name': self.item_name,
            'item_content': self.item_content,
            'item_describe': self.item_describe,
        }



