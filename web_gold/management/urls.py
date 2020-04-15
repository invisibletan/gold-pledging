from django.urls import path
from .views import *

urlpatterns = [
    path('' ,my_login, name='login'),
    path('pledging',pledging ,name='pledging'),
    path('customers', customers, name='customers'),
    path('view_customer/<int:cus_id>', view_customer, name='view_customer'),
    path('view_pledging/<int:pled_id>', view_pledging, name='view_pledging'),
    path('delete_customer/<int:cus_id>', delete_customer, name='delete_customer'),
    path('delete_pledging/<int:pled_id>', delete_pledging, name='delete_pledging'),
    #path('add_pledging', add_pledging, name='add_pledging'),
    path('add_customer', add_customer, name='add_customer'),
    
]