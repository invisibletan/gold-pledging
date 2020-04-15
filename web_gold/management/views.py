from builtins import object
from django.shortcuts import redirect, render
from .models import Customer, Pledging
from .form import CustomerForm
# Create your views here.

def my_login(request):
    return render(request, template_name='login.html')

def pledging(request):
    pledging = Pledging.objects.all()
    return render(request, 'pledging.html', context={'pledging': pledging})

def customers(request):
    customer = Customer.objects.all()
    return render(request, 'customers.html', context={'customer': customer})

def view_customer(request, cus_id):
    view_cus = Customer.objects.get(pk=cus_id)
    return render(request, 'view_customer.html', context={'cus': view_cus})

def view_pledging(request, pled_id):
    view_pled = Pledging.objects.get(pk=pled_id)
    return render(request, 'view_pledging.html', context={'p': view_pled})

def delete_customer(request, cus_id):
    cus = Customer.objects.get(pk=cus_id)
    cus.delete()
    return redirect(to='customers')

def delete_pledging(request, pled_id):
    pled = Pledging.objects.get(pk=pled_id)
    pled.delete()
    return redirect(to='pledging')

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('customers')
    else:
        form = CustomerForm(initial={
            'user_id' : request.user
        })
    return render(request, template_name='add_customer.html',context={'form': form})
#def add_pledging(request):