from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Authenticate
    path('', payment, name='payment'),
    path('inform/', inform_payment, name='inform_payment'),
    path('verify/<int:payment_id>', verify_payment, name='verify_payment'),

]