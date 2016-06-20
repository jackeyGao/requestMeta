import json, uuid
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import _get_new_csrf_key
from web.models import Request
from web.models import URL

# Create your views here.

ALLOW_KEYS = (
        'REQUEST_METHOD',
        'SERVER_PROTOCOL',
        'CONTENT_LENGTH',
        'REMOTE_ADDR',
        'CONTENT_TYPE'
        )

def set_cookie(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        expires = datetime.now() + timedelta(days=7)
        if request.COOKIES.get('user', None):
            _tk = request.COOKIES.get('user', None)
        else:
            _tk = _get_new_csrf_key()

        response = fn(*args, **kwargs)
        response.set_cookie('user', _tk, expires=expires)
        return response
    return wrapper


@csrf_exempt
def receiver(request, url):
    url = get_object_or_404(URL, pk=url)
    meta = request.META
    metas = { k: str(v) for k, v in meta.items() if k in ALLOW_KEYS }
    headers = { k: str(v) for k, v in meta.items() if k.startswith('HTTP')}
    parameters = request.GET or request.POST
    raw_body = request.body

    metas["SCHEME"] = request.scheme

    ob = {}
    ob["url"] = url
    ob["metas"] = metas
    ob["method"] = request.method
    ob["headers"] = headers
    ob["parameters"] = parameters
    ob["body"] = raw_body
    Request(**ob).save()
    return HttpResponse('OK')

@csrf_protect
@set_cookie
def inspect(request, url):
    url = get_object_or_404(URL, pk=url)
    qs = Request.objects.filter(url=url).order_by('-time')[:30]
    http_host = request.META.get('HTTP_HOST', None)
    return render_to_response('inspect.html', locals())

@csrf_protect
@set_cookie
def create_url(request):
    _tk = request.COOKIES.get('user', None)
    _id = str(uuid.uuid5(uuid.NAMESPACE_DNS, _tk + str(uuid.uuid4())))[:8]
    url = URL(user=_tk, _id=_id)
    url.save()
    return HttpResponse(url.pk)


@csrf_protect
@set_cookie
def index(request):
    if not request.COOKIES.get('user', None):
        return render_to_response('index.html', locals())

    _tk = request.COOKIES.get('user', None)
    urls = URL.objects.filter(user=_tk).order_by('-start_time')[:10]
    for url in urls:
        count = Request.objects.filter(url=url).count()
        if count > 30:
            url.count = 30
        else:
            url.count = count

    return render_to_response('index.html', locals())

