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
from django.contrib.auth.decorators import permission_required, login_required
from .form import AdminForm, CustomerForm, GoldForm, PledgingForm
from .models import Customer, Gold, Log, Pledging
from .serializers import CustomerSerializer, LogSerializer, PledgingSerializer

# Create your views here.



# from background_task import background
# t = 0
# text = 1
# sec = 17
# mint = 3 if (text) else 60
# hour = 1 if (text) else 60
# day = 1 if (text) else 24
# @background()
# def update_queue_status():
#     global t, sec, mint, hour, day
#     if t%(sec*mint*hour*day) == 0:
#         print(t//(sec*mint*hour*day))
#         out_date = Pledging.objects.filter(expire_date__lte=date.today()+ timedelta(days=3),type_pledging=1).exclude(expire_date=date.today())
#         out_date_today = Pledging.objects.filter(expire_date=date.today(),type_pledging=1)

#         out_date_list =list((out_date.values('cus_id__email', 'cus_id__id', 'id', 'expire_date')))
#         out_date_today_list =list((out_date_today.values('cus_id__email', 'cus_id__id', 'id', 'expire_date')))
#         def return_list_dict(out_date_list):
#             cus_list = dict()
#             for od in out_date_list:
#                 cus_id = od["cus_id__id"]
#                 if cus_id in cus_list:
#                     cus_list[cus_id].append(od)
#                 else:
#                     cus_list[cus_id] = [od]
#             return cus_list
#         cus_list = return_list_dict(out_date_list)
#         cus_list_today = return_list_dict(out_date_today_list)


#         def sendmail(cus_list, chk):
#             from_email = settings.EMAIL_HOST_USER
#             for cus in cus_list:
#                 if chk:
#                     message = ", ".join(['รหัสที่ '+str(pledging["id"])+' กำลังจะครบกำหนดสัญญาในวันที่ '+str(pledging["expire_date"].strftime("%d/%m/%Y")) for pledging in cus_list[cus]])
#                     message = 'รายการจำนำ '+ message + ' ' + '\rกรุณาชำระเงินในระยะเวลาที่กำหนด\rโทร : xxx-xxx-xxx'
#                 else:
#                     message = ", ".join([str(pledging["id"]) for pledging in cus_list[cus]])
#                     message = 'รายการจำนำ รหัสที่ '+ message + ' ' + 'ครบกำหนดสัญญาแล้ว\rโทร : xxx-xxx-xxx'
#                 email_list = [cus_list[cus][0]['cus_id__email']]
                

#                 send_mail(
#                 subject='เรียนเพื่อทราบ',
#                 message= message ,
#                 from_email=from_email,
#                 recipient_list=email_list,
#                 fail_silently=False)
#                 print('ส่ง', message)

#         sendmail(cus_list, 1)
#         sendmail(cus_list_today, 0)

#         out_date_today = out_date_today.update(type_pledging=0)
#     t += 1

            
# update_queue_status()
@login_required
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
            next_url = request.POST.get('next_url')
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            context['username'] = username
            context['error'] = 'username or password is invalid'
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url
    return render(request, template_name='login.html', context=context)

@login_required
def my_logout(request):
    logout(request)
    return redirect('login')

@login_required
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
        pledging = pledging.order_by('id')    
        serializer =  PledgingSerializer(pledging, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
@csrf_exempt
@api_view(['GET', 'POST'])  
def customers_api(request):
    if request.method == 'GET':
        # find = request.query_params['find']
       
        # cus = Customer.objects.filter(Q(first_name__icontains=find)|(Q(last_name__icontains=find))|(Q(id__icontains=find)))
        find = request.query_params['find'].split()
        find.append('') if find == [] else 0
        cus = Customer.objects.filter(reduce(lambda x, y: x | y, [(Q(first_name__icontains=word))|(Q(last_name__icontains=word))|(Q(id__icontains=word)) for word in find])).order_by('id')
        serializer =  CustomerSerializer(cus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@login_required
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
        log = log.order_by('-datetime')
        
        serializer =  LogSerializer(log, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def pledging(request):
    return render(request, 'pledging.html')

@login_required
def customers(request):
    return render(request, 'customers.html')

@login_required
def log(request):
    return render(request, 'log.html')


@login_required
def view_customer(request, cus_id):
    view_cus = Customer.objects.get(pk=cus_id)
    view_pledging = Pledging.objects.filter(cus_id=cus_id)
    return render(request, 'view_customer.html', context={'cus': view_cus, 'p': view_pledging})

@login_required
def view_pledging(request, pled_id):
    view_pled = Pledging.objects.get(pk=pled_id)
    
    view_gold = Gold.objects.filter(pledging_id=pled_id)
    return render(request, 'view_pledging.html', context={'p': view_pled, 'gold': view_gold})

@login_required
@csrf_exempt
def delete_customer(request, cus_id):
    if request.method == 'DELETE':
        cus = Customer.objects.get(pk=cus_id)
        cus.delete()
    return HttpResponse(status=200)

@login_required
@csrf_exempt
def delete_pledging(request, pled_id):
    if request.method == 'DELETE':
        pled = Pledging.objects.get(pk=pled_id)
        pled.delete()
    return HttpResponse(status=200)

@login_required
def add_customer(request):
    msg = ''
    cus_id = ''
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            # create user
            user = User.objects.create_user(username = '%05d'%(customer.id))
            user.set_password(customer.citizen_id)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            user.save()
            # relation to user
            customer.user_acc = user
            customer.save()
            msg = 'pass_add'
            cus_id = customer.id
        else:
            msg = 'no_pass'
    else:
        form = CustomerForm(initial={
            'user_id' : request.user
        })
    return render(request, template_name='add_customer.html',context={'form': form, 'status':1, 'msg':msg, 'cus_id':cus_id})

@login_required
def add_pledging(request, customer_id):
    msg = ''
    pled_id = ''
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
            msg = 'pass_add'
            pled_id = pled.id
        else:
            msg = 'no_pass'
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
    return render(request, template_name='add_pledging.html',context={'form': form, 'form2': form2, 'status':1, 'msg':msg, 'pled_id':pled_id})

@login_required
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
            msg = 'pass'
        else:
            msg = 'no_pass'
     
    else:
        form = CustomerForm(initial={
            'cus_id' : cus.id,
            'user_id' : request.user,
            'first_name' : cus.first_name,
            'last_name' : cus.last_name,
            'email' : cus.email,
            'citizen_id' : cus.citizen_id,
            'dob' : cus.dob
        })
    return render(request, template_name='add_customer.html',context={'form': form, 'status':0, 'msg':msg})


@login_required
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
        print(form)
        if form.is_valid() and form2.is_valid():
            
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
            msg = 'pass'
        else:
            msg = 'no_pass'
    else:
        form = PledgingForm(initial={
            'user_id' : request.user,
            'cus_id' : pled.cus_id,
            'pledge_balance' : pled.pledge_balance,
            'contract_term' : pled.contract_term,
            'expire_date' : pled.expire_date,
        })
        form2 = form2(initial=data)
    return render(request, template_name='add_pledging.html',context={'form': form, 'form2': form2,'status':0, 'msg':msg, 'pled_id':pled_id})

@login_required
@csrf_exempt
def delete_gold(request, gold_id):
    if request.method == 'DELETE':
        gold = Gold.objects.get(pk=gold_id)
        gold.delete()
    return HttpResponse(status=200)

@login_required
def edit_admin(request,admin_id):
    msg = ''
    admin = User.objects.get(pk=admin_id)
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            admin.username = form.cleaned_data['username'] 
            admin.first_name=form.cleaned_data['first_name']
            admin.last_name=form.cleaned_data['last_name']
            admin.email=form.cleaned_data['email']
            admin.set_password(form.cleaned_data["password1"])
            admin.save()
            logout(request)
            return redirect('http://127.0.0.1:8000/login/?edit_admit=pass')
        else:
            msg = 'no_pass'
    else:
        form = AdminForm(initial={
            'admin_id': admin.id,
            'username' : admin.username,
            'first_name' : admin.first_name,
            'last_name' : admin.last_name,
            'email' : admin.email,
            
        })
    context = {'form': form, 'msg':msg}
    return render(request, 'edit_admin.html', context)
