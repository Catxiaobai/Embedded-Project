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