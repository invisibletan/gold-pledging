from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Payment
    path('', payment, name='payment'),
    path('select/', select_pledging, name='select_pledging'),
    path('detail/', detail_payment, name='detail_payment'),
    path('inform/<int:payment_id>', inform_payment, name='inform_payment'), 
    path('approve/<int:payment_id>', approve_payment, name='approve_payment'),
    path('reject/<int:payment_id>', reject_payment, name='reject_payment'),
    # Transaction
    path('transaction/add/<int:pled_id>', add_transaction, name='add_transaction'),
    path('redeem/detail/<int:pled_id>', detail_redeemed, name='detail_redeemed'),
]