from django.db import models
from django.contrib.auth.models import User
from django_enumfield import enum
from django.conf import settings
from django.utils.translation import ugettext_lazy
from django.core.validators import MinLengthValidator
from datetime import timedelta, date

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

class GoldType(enum.Enum):
    necklace = 0
    Bracelet = 1
    ring = 2
    bracelet = 3
    __labels__ = {
        necklace: ugettext_lazy("สร้อยคอ"),
        Bracelet: ugettext_lazy("สร้อยข้อมือ"),
        ring: ugettext_lazy("แหวน"),
        bracelet: ugettext_lazy("กำไล"),
    }
class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    citizen_id = models.CharField(max_length=13,validators=[MinLengthValidator(13)], null=False, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    dob = models.DateField(auto_now_add=False,blank=False)

class Pledging(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pledge_balanca = models.IntegerField(null=False)
    contract_term = models.IntegerField(null=False)
    pledge_date = models.DateField(auto_now_add=True,blank=False,null=False)
    expire_date = models.DateField(auto_now_add=False,null=True)
    type_pledging = enum.EnumField(PledgingType, default=PledgingType.in_contract)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expire_date = date.today() + timedelta(days=self.contract_term)
        super(Pledging, self).save(*args, **kwargs)



class Gold(models.Model):
    pledging_id = models.ForeignKey(Pledging, on_delete=models.CASCADE)
    weight = models.FloatField(blank=False,null=False)
    goldtype =  enum.EnumField(GoldType, default=GoldType.necklace)

class Redeemed(Pledging):
    
    first_name = models.CharField(null=False, max_length=255)
    last_name = models.CharField(null=False, max_length=255)
    citizen_id = models.CharField(max_length=13, null=False, unique=True)
    redeem_date = models.DateField(auto_now_add=True,blank=False,null=False)

class Log(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime = models.DateField(auto_now_add=True,blank=False,null=False)
    detail = models.TextField()


