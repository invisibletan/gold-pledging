#def add_pledging(request):
import email
from builtins import object
from datetime import date, timedelta
from functools import reduce

from django.conf import settings
# from background_task import background
from django.contrib.admin.helpers import AdminForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .form import AdminForm, CustomerForm, GoldForm, PledgingForm
from .models import Customer, Gold, Log, Pledging
from .serializers import CustomerSerializer, LogSerializer, PledgingSerializer

# Create your views here.


# from background_task import background
# t = 0
# k = 1
# @background(schedule=1)
# def update_queue_status():
#     global t
#     global k
#     print(t)
#     out_date = Pledging.objects.filter(expire_date=date.today()).exclude(type_pledging=0)
#     email =[i['cus_id__email'] for i in list(out_date.values('cus_id__email'))]
#     email = list(set(email))
#     from_email = settings.EMAIL_HOST_USER
#     if k:
#         send_mail(
#         subject='รายการจำนำหมดสัญญา',
#         message='ลูกค้าไม่สามารถไถ่รายการจำนำ ภายในระยะเวลาสัญญา',
#         from_email=from_email,
#         recipient_list=email,
#         fail_silently=False)
#         print(email)
#         k = 0
#     out_date = out_date.update(type_pledging=0)
#     t += 1

            
# update_queue_status(repeat=1)

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print(request.user)
    return render(request, template_name='index.html')

def my_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context['username'] = username
            context['error'] = 'username or password is invalid'
    return render(request, template_name='login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

@csrf_exempt
@api_view(['GET', 'POST'])
def pledging_api(request):
    if request.method == 'GET':
        # find = request.query_params['find']
        if 'customer' in [group.name for group in request.user.groups.all()]:
            customer = Customer.objects.get(user_acc=request.user)
            pledging = Pledging.objects.filter(cus_id=customer)
        else:
            pledging = Pledging.objects.all()

        find = request.query_params['find'].split()
        find.append('') if find == [] else 0
        pledging = pledging.filter(reduce(lambda x, y: x | y, [(Q(cus_id__first_name__icontains=word))|(Q(cus_id__last_name__icontains=word))|(Q(id__icontains=word)) for word in find]))
        chk_out = int(request.query_params['chk_out'])
        chk_in = int(request.query_params['chk_in'])
        chk_re = int(request.query_params['chk_re'])
        s_date = request.query_params['s_date']
        e_date = request.query_params['e_date']
        pled_date = int(request.query_params['pled_date'])
        pledging = pledging.filter(type_pledging__in=[chk_out, chk_in, chk_re])
        print(pled_date)
        if (pled_date):
            if s_date != '' and s_date is not None:
                pledging = pledging.filter(pledge_date__gte=s_date)
            if e_date  != '' and e_date is  not None:
                pledging = pledging.filter(pledge_date__lte=e_date)
        else:
            print('wow')
            if s_date != '' and s_date is not None:
                pledging = pledging.filter(expire_date__gte=s_date)
            if e_date  != '' and e_date is not None:
                pledging = pledging.filter(expire_date__lte=e_date)
            
        serializer =  PledgingSerializer(pledging, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])  
def customers_api(request):
    if request.method == 'GET':
        # find = request.query_params['find']
       
        # cus = Customer.objects.filter(Q(first_name__icontains=find)|(Q(last_name__icontains=find))|(Q(id__icontains=find)))
        find = request.query_params['find'].split()
        find.append('') if find == [] else 0
        cus = Customer.objects.filter(reduce(lambda x, y: x | y, [(Q(first_name__icontains=word))|(Q(last_name__icontains=word))|(Q(id__icontains=word)) for word in find]))
        serializer =  CustomerSerializer(cus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
@csrf_exempt
@api_view(['GET', 'POST'])
def log_api(request):
    if request.method == 'GET':
        # find = request.query_params['find']
        if 'customer' in [group.name for group in request.user.groups.all()]:
            customer = Customer.objects.get(user_acc=request.user)
            log = Log.objects.filter(cus_id=customer)
        else:
            log = Log.objects.all()
        find = request.query_params['find'].split()
        find.append('') if find == [] else 0
        log = log.filter(reduce(lambda x, y: x | y, [(Q(cus_id__first_name__icontains=word))|(Q(cus_id__last_name__icontains=word))|(Q(user_id__last_name__icontains=word))|(Q(user_id__first_name__icontains=word)) for word in find]))
        # log = log.filter(Q(cus_id__first_name__icontains=find)|(Q(cus_id__last_name__icontains=find)))
        chk_add = int(request.query_params['chk_add'])
        chk_re = int(request.query_params['chk_re'])
        chk_redeem = int(request.query_params['chk_redeem'])
        chk_sla = int(request.query_params['chk_sla'])
        chk_get = int(request.query_params['chk_get'])
        s_date = request.query_params['s_date'].split('-')
        e_date = request.query_params['e_date'].split('-')

        log = log.filter(detail__in=[chk_add, chk_re, chk_redeem, chk_sla, chk_get])
        if '' not in s_date  and s_date is not None:
            log = log.filter(datetime__year__gte=s_date[0],datetime__month__gte=s_date[1],datetime__day__gte=s_date[2])
        if '' not in e_date  and e_date is not None:
            log = log.filter(datetime__year__lte=e_date[0],datetime__month__lte=e_date[1],datetime__day__lte=e_date[2])
        
        
        serializer =  LogSerializer(log, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



def pledging(request):
    return render(request, 'pledging.html')

def customers(request):
    return render(request, 'customers.html')

def log(request):
    return render(request, 'log.html')



def view_customer(request, cus_id):
    view_cus = Customer.objects.get(pk=cus_id)
    view_pledging = Pledging.objects.filter(cus_id=cus_id)
    return render(request, 'view_customer.html', context={'cus': view_cus, 'p': view_pledging})

def view_pledging(request, pled_id):
    view_pled = Pledging.objects.get(pk=pled_id)
    
    view_gold = Gold.objects.filter(pledging_id=pled_id)
    return render(request, 'view_pledging.html', context={'p': view_pled, 'gold': view_gold})

@csrf_exempt
def delete_customer(request, cus_id):
    if request.method == 'DELETE':
        cus = Customer.objects.get(pk=cus_id)
        cus.delete()
    return HttpResponse(status=200)
@csrf_exempt
def delete_pledging(request, pled_id):
    if request.method == 'DELETE':
        pled = Pledging.objects.get(pk=pled_id)
        pled.delete()
    return HttpResponse(status=200)

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            # create user
            user = User.objects.create_user(username = '%d'%(customer.id))
            user.set_password(customer.citizen_id)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            user.save()
            # relation to user
            customer.user_acc = user
            customer.save()
            return redirect('view_customer', cus_id=customer.id)
    else:
        form = CustomerForm(initial={
            'user_id' : request.user
        })
    return render(request, template_name='add_customer.html',context={'form': form, 'status':1})

def add_pledging(request, customer_id):
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
            user = User.objects.get(pk=request.user.id)
            log = Log.objects.create(
                    user_id=user,
                    detail=4,
                    cus_id=pled.cus_id)
            return redirect('view_customer', cus_id=pled.cus_id.id)
    else:
        if customer_id:
            form = PledgingForm(initial={
            'user_id' : request.user,
            'cus_id' : customer_id
            })
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
        print(cus.id)
        form = CustomerForm(initial={
            'cus_id' : cus.id,
            'user_id' : request.user,
            'first_name' : cus.first_name,
            'last_name' : cus.last_name,
            'email' : cus.email,
            'citizen_id' : cus.citizen_id,
            'dob' : cus.dob
        })
    print(form)
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
            pled.pledge_balance=request.POST.get('pledge_balance')
            pled.contract_term=request.POST.get('contract_term')
            if  date.today() !=date.today() + timedelta(days=int(pled.contract_term)):
                pled.type_pledging=1
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
            'pledge_balance' : pled.pledge_balance,
            'contract_term' : pled.contract_term,
            'expire_date' : pled.expire_date,
        })
        form2 = form2(initial=data)
    return render(request, template_name='add_pledging.html',context={'form': form, 'form2': form2,'status':0, 'msg':''})


def delete_gold(request, gold_id, pled_id):
    gold = Gold.objects.get(pk=gold_id)
    gold.delete()
    return redirect('view_pledging', pled_id=pled_id)

def edit_admin(request,admin_id):
    admin = User.objects.get(pk=admin_id)
    msg = ''
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            admin.username = form.cleaned_data['username'] 
            admin.first_name=form.cleaned_data['first_name']
            admin.last_name=form.cleaned_data['last_name']
            admin.email=form.cleaned_data['email']
            admin.password=form.cleaned_data['password1']
            admin.save()
            msg = 'แก้ไขสำเร็จ'
        else:
            msg = ''
    else:
        form = AdminForm(initial={
            'admin_id': admin.id,
            'username' : admin.username,
            'first_name' : admin.first_name,
            'last_name' : admin.last_name,
            'email' : admin.email,
            
        })
    context = {'form': form, 'msg': msg}
    return render(request, 'edit_admin.html', context)
