# -*- coding: utf-8 -*-
'''
File Name: web/templatetags/tools.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 四  6/16 10:52:51 2016
'''
import json
import arrow
from django.conf import settings
from django import template

register = template.Library()

@register.filter
def humanize(time):
    if time is None:
        return None
    return arrow.get(time, settings.TIME_ZONE).humanize()

@register.filter
def value(jsonstring, key):
    if isinstance(jsonstring, dict):
        data = jsonstring
    else:
        data = json.loads(jsonstring)
    value= data.get(key, None)
    if value:
        return value.strip()
    return value 

@register.filter
def is_json(jsonstring):
	try:
	    data = json.loads(jsonstring)
	except Exception as e:
		return False
	return True

@register.filter
def to_json(jsonstring):
	try:
	    data = json.loads(jsonstring)
	    return json.dumps(data, indent=2, ensure_ascii=False)
	except Exception as e:
		return None

