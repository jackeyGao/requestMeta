from __future__ import unicode_literals
import json
from django.db import models
from jsonfield import JSONField

# Create your models here.

class URL(models.Model):
    _id = models.CharField(max_length=45, primary_key=True)
    user = models.CharField(max_length=45, default=None)
    start_time = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self._id

    def __unicode__(self):
        return unicode(self.__str__())


class Request(models.Model):
    url = models.ForeignKey(URL)
    time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, default=None)
    metas = JSONField(default=None)
    headers = JSONField()
    parameters = JSONField()
    body = models.TextField(default="")

    def to_json(self):
        ob = {}
        ob["metas"] = self.metas
        ob["parameters"] = self.parameters
        ob["headers"] = self.headers
        return json.dumps(ob, indent=2, ensure_ascii=False)

    def __str__(self):
        return self.url._id

    def __unicode__(self):
        return unicode(self.__str__())


