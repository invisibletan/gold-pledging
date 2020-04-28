from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Register your models here.

class GoldAdmin(admin.ModelAdmin):
    list_display = ['id', 'pledging_id','weight', 'goldtype']
    list_per_page = 10
admin.site.register(Permission)
admin.site.register(Customer)
admin.site.register(Pledging)
admin.site.register(Gold, GoldAdmin)
admin.site.register(Redeemed)
admin.site.register(Log)
