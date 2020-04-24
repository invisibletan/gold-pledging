from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Authenticate
    path('inform/', inform_payment, name='inform_payment'),
]