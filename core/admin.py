from django.contrib import admin

from core.models import Config, ZellularTransaction

admin.site.register(Config)
admin.site.register(ZellularTransaction)
