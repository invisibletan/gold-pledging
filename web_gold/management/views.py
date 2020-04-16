#def add_pledging(request):
import email
from builtins import object

from django.shortcuts import redirect, render

from .form import CustomerForm, PledgingForm,GoldForm
from .models import Customer, Pledging, Gold
from datetime import timedelta, date
from django.forms import formset_factory
# Create your views here.

def my_login(request):
    update_status()
    return render(request, template_name='login.html')

def pledging(request):
    pledging = Pledging.objects.all()
    return render(request, 'pledging.html', context={'pledging': pledging})

def customers(request):
    customer = Customer.objects.all()
    return render(request, 'customers.html', context={'customer': customer})

def view_customer(request, cus_id):
    view_cus = Customer.objects.get(pk=cus_id)
    view_pledging = Pledging.objects.filter(cus_id=cus_id)
    return render(request, 'view_customer.html', context={'cus': view_cus, 'p': view_pledging})

def view_pledging(request, pled_id):
    view_pled = Pledging.objects.get(pk=pled_id)
    view_gold = Gold.objects.filter(pledging_id=pled_id)
    return render(request, 'view_pledging.html', context={'p': view_pled, 'gold': view_gold})

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

def add_pledging(request):
    form2 = formset_factory(GoldForm)
    if request.method == 'POST':
        form = PledgingForm(request.POST)
        form2 = form2(request.POST)

        if form.is_valid() and form2.is_valid():
            pled = form.save()
       
            for form in form2:
                if form.cleaned_data.get('weight'):
                    gold = Gold.objects.create(
                    pledging_id=Pledging.objects.get(pk=pled.id),
                    weight=form.cleaned_data['weight'],
                    goldtype=form.cleaned_data['goldtype'])
            
            return redirect('pledging')
    else:
        form = PledgingForm(initial={
            'user_id' : request.user
        })
        
    return render(request, template_name='add_pledging.html',context={'form': form, 'form2': form2, 'status':1})

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

def edit_pledging(request, pled_id):
    
    pled = Pledging.objects.get(pk=pled_id)
    gold = Gold.objects.filter(pledging_id=pled_id)
    num = len(gold)
    data = []
    form2 = formset_factory(GoldForm, max_num=num)
    for i in gold:
        gold_dict = {
            'pledging_id':pled_id,
            'weight': i.weight,
            'goldtype':i.goldtype,
            'gold_id':i.id
        }
        data.append(gold_dict)
    msg = ''
    if request.method == 'POST':
        form = PledgingForm(request.POST)
        form2 = form2(request.POST)
        if form.is_valid() and form2.is_valid():
            pled.cus_id=Customer.objects.get(pk=request.POST.get('cus_id'))
            pled.pledge_balanca=request.POST.get('pledge_balanca')
            pled.contract_term=request.POST.get('contract_term')
            pled.expire_date=pled.pledge_date + timedelta(days=int(pled.contract_term))
            pled.save()
            
            for f in form2:
                if f.cleaned_data.get('gold_id'):
                    if f.cleaned_data.get('weight'):
                        g = Gold.objects.get(pk=f.cleaned_data['gold_id'])
                        g.weight = f.cleaned_data['weight']
                        g.goldtype =  f.cleaned_data['goldtype']
                        g.save()
                else:
                    if f.cleaned_data.get('weight'):
                        gold = Gold.objects.create(
                        pledging_id=Pledging.objects.get(pk=pled.id),
                        weight=f.cleaned_data['weight'],
                        goldtype=f.cleaned_data['goldtype'])
            msg = 'แก้ไขสำเร็จ'
            return redirect('view_pledging', pled_id=pled_id)
        else:
            msg = ''
    else:
        form = PledgingForm(initial={
            'user_id' : request.user,
            'cus_id' : pled.cus_id,
            'pledge_balanca' : pled.pledge_balanca,
            'contract_term' : pled.contract_term,
            'expire_date' : pled.expire_date,
        })
        form2 = form2(initial=data)
    return render(request, template_name='add_pledging.html',context={'form': form, 'form2': form2,'status':0, 'msg':''})


def delete_gold(request, gold_id, pled_id):
    gold = Gold.objects.get(pk=gold_id)
    gold.delete()
    return redirect('view_pledging', pled_id=pled_id)

def edit_admin(request):
    pass
