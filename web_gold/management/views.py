#def add_pledging(request):
import email
from builtins import object

from django.shortcuts import redirect, render

from .form import CustomerForm
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
    return render(request, template_name='add_customer.html',context={'form': form, 'status':1})

def edit_customer(request, cus_id):
    cus = Customer.objects.get(pk=cus_id)
    msg = ''
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cus.first_name=request.POST.get('first_name')
            cus.last_name=request.POST.get('last_name')
            cus.email=request.POST.get('email')
            cus.citizen_id=request.POST.get('citizen_id')
            cus.dob=request.POST.get('dob')
            cus.save()
            msg = 'แก้ไขสำเร็จ'
            return redirect('customers')
        else:
            msg = ''
    else:
        form = CustomerForm(initial={
            'user_id' : request.user,
            'first_name' : cus.first_name,
            'last_name' : cus.last_name,
            'email' : cus.email,
            'citizen_id' : cus.citizen_id,
            'dob' : cus.dob
        })
    return render(request, template_name='add_customer.html',context={'form': form, 'status':0, 'msg':''})
