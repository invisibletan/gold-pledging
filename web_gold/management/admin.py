from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(Permission)
admin.site.register(Customer)
admin.site.register(Pledging)
admin.site.register(Gold)
admin.site.register(Redeemed)
admin.site.register(Log)