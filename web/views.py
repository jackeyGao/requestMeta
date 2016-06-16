import json, uuid
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
        'wsgi.url_scheme',
        'CONTENT_TYPE'
        )

def set_cookie(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.COOKIES.get('user', None):
            _tk = request.COOKIES.get('user', None)
        else:
            _tk = _get_new_csrf_key()

        response = fn(*args, **kwargs)
        response.set_cookie('user', _tk)
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
    qs = Request.objects.filter(url=url).order_by('-time')
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
    if request.COOKIES.get('user', None):
        _tk = request.COOKIES.get('user', None)
    else:
        _tk = _get_new_csrf_key()

    urls = URL.objects.filter(user=_tk).order_by('-start_time')
    for url in urls:
        count = Request.objects.filter(url=url).count()
        url.count = count

    #urls = sorted(urls, key=lambda u:u.count,reverse=False)
    response = render_to_response('index.html', locals())
    return response

