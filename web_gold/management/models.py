from django.db import models
from django_enumfield import enum
# Create your models here..
class status(enum.Enum):
    EXPIRED = 0
    IN_CONTRACT = 1
    REDEEMED = 2


class status_pay(enum.Enum):
    Renew_Contract = 0
    Redeem = 1


class CUSTOMER(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    dob = models.DateField(auto_now=False)
    citizen_id = models.CharField(max_length=254)

class PLEDGING(models.Model):
    customer_id = models.ForeignKey(CUSTOMER, on_delete=models.PROTECT, blank=True,null=True)
    pledge_balance = models.IntegerField()
    pledge_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(auto_now_add=True)
    contract_term = models.IntegerField()
    type_pled = enum.EnumField(status, default=status.EXPIRED)


class REDEEMED(PLEDGING):
    redeem_date = models.DateTimeField(auto_now_add=True)
    

class PAYMENT(models.Model):
    pay_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    payment_for = enum.EnumField(status_pay, default=status_pay.Renew_Contract)
    pay_pled = models.ManyToManyField(PLEDGING, through='PAYMENT_PLEDGING')


class GOLD(models.Model):
    pledging_id = models.ForeignKey(CUSTOMER, on_delete=models.PROTECT, blank=False,null=False)
    weight = models.FloatField()


    

class PAYMENT_PLEDGING(models.Model):
    pled_id = models.ForeignKey(PLEDGING, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(PAYMENT, on_delete=models.CASCADE)
    amount = models.IntegerField()


