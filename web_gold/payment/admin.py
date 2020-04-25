from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(Payment)
admin.site.register(Online)
# admin.site.register(Offline)
admin.site.register(Transaction)
admin.site.register(Re_contract)