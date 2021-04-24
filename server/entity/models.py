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




