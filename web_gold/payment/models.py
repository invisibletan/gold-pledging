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
    add_pledging = 4
    __labels__ = {
        re_contract: ugettext_lazy("ต่อดอก"),
        redeem: ugettext_lazy("ไถ่คืน"),
        slacken: ugettext_lazy("ผ่อนจ่าย"),
        getmore: ugettext_lazy("เอาเพิ่ม"),
        add_pledging: ugettext_lazy("ทำรายการจำนำ"),
    }

class Payment(models.Model):
    type_payment = enum.EnumField(PaymentType, default=PaymentType.online)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    total_amount = models.IntegerField(null=False)
    pay_date = models.DateField(auto_now_add=True, blank=False, null=False)

class Online(Payment):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, default=None, null=True)
    cus_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = enum.EnumField(Status, default=Status.wait)
    picture = models.ImageField(upload_to='payments/', default=None, null=True)

class Offline(Payment):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    cus_id = models.ForeignKey(Customer, on_delete=models.PROTECT)

class Transaction(models.Model):
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, default=None, null=True)
    pledging_id = models.ForeignKey(Pledging, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    trantype = enum.EnumField(Trantype, default=Trantype.re_contract)

class Recontract(models.Model):
    pledging_id = models.ForeignKey(Pledging, on_delete=models.CASCADE)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=False, blank=False, null=False)
