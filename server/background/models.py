from django.db import models

from entity.models import Item, Personnel


# Create your models here.


#  项目普通人员表
class ItemPerson(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    temp = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.id,
            'item_name': self.item.name,
            'personnel': self.personnel.id,
            'temp': self.temp,
            'name': self.personnel.name,
            'account': self.personnel.account,
            'authority': self.personnel.authority,
            'team': self.personnel.team,  # 所属单位
        }


class Node(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.TextField(default='', unique=True)
    label = models.TextField(default='', unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item.id,
            'name': self.name,
            'label': self.label,
        }

    def to_show(self):
        return {
            'text': self.name,
            'label': self.label
        }


class Edge(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.TextField(default='')
    src = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='src')
    tgt = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='tgt')
    event = models.TextField(default='')
    condition = models.TextField(default='')
    action = models.TextField(default='')

    def to_dict(self):
        return {
            'id': self.id,
            'item_id': self.item.id,
            'name': self.name,
            'src': self.src.name,
            'tgt': self.tgt.name,
            'event': self.event,
            'action': self.action,
            'condition': self.condition,
        }
    def to_show(self):
        return {
            'text': self.name,
            'from': self.src.name,
            'to': self.tgt.name,
            'event': self.event,
            'action': self.action,
            'condition': self.condition,
        }