#!/bin/bash
# File Name: docker-entrypoint.sh
# Author: JackeyGao
# mail: gaojunqi@outlook.com
# Created Time: 四  6/16 14:41:51 2016


/code/manage.py migrate

echo "from django.contrib.auth.models import User
if not User.objects.filter(username='admin').count():
    User.objects.create_superuser('admin', 'admin@example.com', 'pass')
" | python manage.py shell


/usr/local/bin/gunicorn requestMeta.wsgi:application -w 2 -b :8000
