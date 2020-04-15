from django.urls import path
from .views import *

urlpatterns = [
    path('' ,my_login, name='login'),
    path('pledging',pledging ,name='pledging'),
    path('customers', customers, name='customers'),
    path('view_customer', view_customer, name='view_customer'),
]