from builtins import object
from django.shortcuts import redirect, render
from .models import Customer, Pledging
# Create your views here.

def my_login(request):
    return render(request, template_name='login.html')

def pledging(request):
    pledging = Pledging.objects.all()
    return render(request, 'pledging.html', context={'pledging': pledging})

def customers(request):
    customer = Customer.objects.all()
    return render(request, 'customers.html', context={'customer': customer})

def view_customer(request):
    return render(request, 'view_customer.html')