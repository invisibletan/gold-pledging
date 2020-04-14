from builtins import object
from django.shortcuts import redirect, render
from .models import Customer, Pledging
# Create your views here.

def my_login(request):
    return render(request, template_name='login.html')

def view_pledging(request):
    pledging = Pledging.objects.all()
    return render(request, 'view_pledging.html', context={'pledging': pledging})

def view_customer(request):
    customer = Customer.objects.all()
    return render(request, 'view_customer.html', context={'customer': customer})
