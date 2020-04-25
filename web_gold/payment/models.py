from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
from management.models import *
# Create your models here.
class PaymentType(enum.Enum):
    online = 0
    offline = 1
    __labels__ = {
        online: ugettext_lazy("ออนไลน์"),
        offline: ugettext_lazy("ออฟไลน์"),
    }
class Status(enum.Enum):
    wait = 0
    approve = 1
    reject = 2
    __labels__ = {
        wait: ugettext_lazy("รอดำเนินการ"),
        approve: ugettext_lazy("ยืนยันเรียบร้อย"),
        reject: ugettext_lazy("ปฎิเสธการทำรายการ"),
    }
class Trantype(enum.Enum):
    re_contract = 0
    redeem = 1
    slacken = 2
    getmore = 3
    __labels__ = {
        re_contract: ugettext_lazy("ต่อดอก"),
        redeem: ugettext_lazy("ไถ่คืน"),
        slacken: ugettext_lazy("ผ่อนจ่าย"),
        getmore: ugettext_lazy("เอาเพิ่ม"),
    }

class Payment(models.Model):
    type_payment = enum.EnumField(PaymentType, default=PaymentType.offline)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    total_amount = models.IntegerField(null=False)
    pay_date = models.DateField(auto_now_add=True,blank=False,null=False)

class Online(Payment):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    cus_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = enum.EnumField(Status, default=Status.wait)

class Offline(Payment):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    cus_id = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Transaction(models.Model):
    payment_id = models.ForeignKey(Payment, on_delete=models.PROTECT)
    amount = models.IntegerField(null=False)
    pledging_id = models.ForeignKey(Pledging, on_delete=models.PROTECT)
    trantype = enum.EnumField(Trantype, default=Trantype.redeem)

class Re_contract(Transaction):
    start_date = models.DateField(auto_now_add=True,blank=False,null=False)
