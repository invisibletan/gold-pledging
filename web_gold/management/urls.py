from django.urls import path
from .views import *

urlpatterns = [
    path('' ,my_login, name='login'),
    path('view_pledging',view_pledging ,name='view_pledging'),
    path('view_customer', view_customer, name='view_customer')
]