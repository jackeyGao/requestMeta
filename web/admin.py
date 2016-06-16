from django.contrib import admin
from web.models import URL, Request

# Register your models here.


class URLAdmin(admin.ModelAdmin):
    list_display = ('__str__', '_id', 'start_time') 


class RequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'time')


admin.site.register(URL, URLAdmin)
admin.site.register(Request, RequestAdmin)
