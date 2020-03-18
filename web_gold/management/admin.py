from django.contrib import admin
from .models import CUSTOMER,PLEDGING,REDEEMED,PAYMENT,GOLD,PAYMENT_PLEDGING
from log.models import LOG
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
# Register your models here.
admin.site.register(LOG)
admin.site.register(PLEDGING)
admin.site.register(REDEEMED)
admin.site.register(PAYMENT)
admin.site.register(GOLD)
admin.site.register(PAYMENT_PLEDGING)