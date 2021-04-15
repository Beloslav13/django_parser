from django.contrib import admin

# Register your models here.
from .models import ApacheLogData


class ApacheLogDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'created_log', 'http_method', 'url', 'response_code', 'response_size')
    list_display_links = ('id', 'ip_address', 'created_log', 'http_method', 'url', 'response_code', 'response_size')
    list_filter = ('created_log', 'http_method', 'response_code')
    search_fields = ('id', 'http_method', 'response_code', 'ip_address')


admin.site.register(ApacheLogData, ApacheLogDataAdmin)
