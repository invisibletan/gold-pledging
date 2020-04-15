from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
from django.conf import settings
from django.utils.translation import ugettext_lazy
# Create your models here.
class PledgingType(enum.Enum):
    expired = 0
    in_contract = 1
    redeem = 2
    __labels__ = {
        expired: ugettext_lazy("หมดสัญญา"),
        in_contract: ugettext_lazy("อยู่ในสัญญา"),
        redeem: ugettext_lazy("ไถ่คืนเรียบร้อย")
    }

class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    citizen_id = models.CharField(max_length=13, null=False)
    email = models.EmailField(max_length=254)
    dob = models.DateField(auto_now_add=False,blank=False)

class Pledging(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    cus_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    pledge_balanca = models.IntegerField(null=False)
    contract_term = models.IntegerField(null=False)
    pledge_date = models.DateField(auto_now_add=True,blank=False,null=False)
    expire_date = models.DateField(auto_now_add=False,blank=False,null=False)
    type_pledging = enum.EnumField(PledgingType, default=PledgingType.in_contract)

class Gold(models.Model):
    pledging_id = models.ForeignKey(Pledging, on_delete=models.PROTECT)
    weight = models.FloatField(null=False)

class Redeemed(Pledging):
    
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    citizen_id = models.CharField(max_length=13, null=False)
    redeem_date = models.DateField(auto_now_add=True,blank=False,null=False)

class Log(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime = models.DateField(auto_now_add=True,blank=False,null=False)
    detail = models.TextField()


