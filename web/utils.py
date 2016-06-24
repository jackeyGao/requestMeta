# -*- coding: utf-8 -*-
'''
File Name: web/utils.py
Author: JackeyGao
mail: gaojunqi@outlook.com
Created Time: 五  6/24 12:56:14 2016
'''


def get_domain_from_wsgirequest(request):
    scheme = request.scheme
    http_host = request.META["HTTP_HOST"]
    return '%s://%s' % (scheme, http_host)
