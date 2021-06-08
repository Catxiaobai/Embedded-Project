from django.db import models

from entity.models import Paths, Item


#  路径数据表
class PathsData(models.Model):
    paths = models.ForeignKey(Paths, on_delete=models.CASCADE)
    data = models.TextField(default='', blank=True)
    type2 = models.TextField(default='', blank=True)
    name = models.TextField(default='', blank=True)

    def to_dict(self):
        return {
            'id': self.id,
            'path_id': self.paths.id,
            'path': self.paths.path,
            'data': self.data,
            'item_id': self.paths.item.id,
            'type2': self.type2,
            'name': self.name,
        }



