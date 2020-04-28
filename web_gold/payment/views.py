from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import redirect, render

from management.models import Customer, Gold, Pledging, PledgingType, Log, Redeemed
from management.form import RedeemedForm
from .models import Online, Payment, Status, Transaction, Recontract

import math

RATE = 0.03

# useful functions

def lasted_date(pledging):
    """ if it was recontracted, get lasted date form Recontract model """
    recontract = Recontract.objects.filter(pledging_id=pledging)
    if recontract:
        return recontract.latest('start_date').start_date
    return pledging.pledge_date

def redeemed_price(pledging):
    """ return redeem price """
    balance = pledging.pledge_balance
    days = max((datetime.now().date() - lasted_date(pledging)).days, 1)
    return balance + balance*(math.ceil(days/10)/3*(1+(days>10)+(days>20)))/100

def create_recontract_trans(transaction, user):
    pledging = transaction.pledging_id
    days = transaction.amount/(pledging.pledge_balance*RATE)*30
    # update contract_term and expire_date
    pledging.contract_term += days
    pledging.expire_date = pledging.expire_date+timedelta(days=days)
    pledging.save()
    # create recontract
    recontract = Recontract.objects.create(
        pledging_id=pledging,
        transaction_id=transaction, 
        start_date=lasted_date(pledging)+timedelta(days=days),
    )
    log = Log.objects.create(user_id=user, detail=transaction.trantype, cus_id=pledging.cus_id)

def create_redeem_trans(pledging, user, data):
    # update type_pledging
    pledging.type_pledging = 2
    pledging.save()
    # create redeemed
    if data:
        redeemed = Redeemed.objects.create(
            pledging_id=pledging,
            first_name=data['first_name'],
            last_name=data['last_name'],
            citizen_id=data['citizen_id'],
        )
    else:
        redeemed = Redeemed.objects.create(
            pledging_id=pledging,
            first_name=pledging.cus_id.first_name,
            last_name=pledging.cus_id.last_name,
            citizen_id=pledging.cus_id.citizen_id,
        )

def create_new_pledging(old_pledging, user, amount, day):
    """ create new pledging without save log """
    new_pledging = Pledging.objects.create(
        user_id=user,
        cus_id=old_pledging.cus_id,
        pledge_balance=amount,
        contract_term=day,
    )
    for old_gold in Gold.objects.filter(pledging_id=old_pledging):
        new_gold = Gold.objects.create(
            pledging_id=new_pledging,
            weight=old_gold.weight,
            goldtype=old_gold.goldtype,
        )
    return str(new_pledging)

def create_slacken_trans(transaction, user, amount, day):
    old_pledging = transaction.pledging_id
    # redeem old pledging
    create_redeem_trans(old_pledging, user, {})
    # pledging new pledging
    new_pledge_id = create_new_pledging(old_pledging, user, old_pledging.pledge_balance-amount, day)
    log = Log.objects.create(user_id=user, detail=transaction.trantype, cus_id=old_pledging.cus_id,)
    return new_pledge_id

def create_getmore_trans(transaction, user, amount, day):
    old_pledging = transaction.pledging_id
    # redeem old pledging
    create_redeem_trans(old_pledging, user, {})
    # pledging new pledging
    new_pledge_id = create_new_pledging(old_pledging, user, old_pledging.pledge_balance+amount, day)
    log = Log.objects.create(user_id=user, detail=transaction.trantype, cus_id=old_pledging.cus_id,)
    return new_pledge_id

# Create your views here.

@login_required
def payment(request):
    if request.user.is_staff:
        context = {'payment': Online.objects.all().order_by('-pk')}
    else:
        customer = Customer.objects.get(user_acc=request.user)
        context = {'payment': Online.objects.filter(cus_id=customer).order_by('-pk')}
    return render(request, template_name='payment.html', context=context)

@login_required
def select_pledging(request):
    context = {}
    customer = Customer.objects.get(user_acc=request.user)
    context['pledging'] = Pledging.objects.filter(cus_id=customer).filter(type_pledging=PledgingType.in_contract)
    context['gold'] = {p.id: Gold.objects.filter(pledging_id=p) for p in context['pledging']}
    if not context['pledging']:
        return redirect('view_customer', customer.id)
    if request.method == 'POST':
        if request.POST.getlist('selected'):
            request.session['selected'] = request.POST.getlist('selected')
            return redirect('detail_payment')
        else:
            # alert 'no selected pledging'
            pass
    return render(request, template_name='select_pledging.html', context=context)

@login_required
def detail_payment(request):
    """ detail before create payment (for customer only) """
    context = {'type': 'detail'}
    customer = Customer.objects.get(user_acc=request.user)
    try:
        context['selected'] = request.session['selected']
    except KeyError:
        return redirect('select_pledging')
    context['detail'] = [{
        'pledge_id': pledge_id,
        'gold': Gold.objects.filter(pledging_id=pledge_id),
        'balance': Pledging.objects.get(id=pledge_id).pledge_balance,
        'interest': Pledging.objects.get(id=pledge_id).pledge_balance*RATE,
    } for pledge_id in context['selected']]
    if request.method == 'POST':
        total_amount = 0
        amount_list = request.POST.getlist('amount')
        mount_list = request.POST.getlist('month')
        # validate
        is_valid =  list()
        for i in range(len(context['selected'])):
            pledge_id = context['selected'][i]
            amount = float(amount_list[i])
            pledge_balance = amount/float(mount_list[i])/RATE
            total_amount += amount
            is_valid += [Pledging.objects.get(id=pledge_id).pledge_balance == pledge_balance]
            print(amount)
        if all(is_valid):
            # create payment
            payment = Online.objects.create(
                first_name=customer.first_name,
                last_name=customer.last_name,
                total_amount=total_amount,
                cus_id=customer,
            )
            # create transactions
            for i in range(len(context['selected'])):
                pledge_id = context['selected'][i]
                transaction = Transaction.objects.create(
                    payment_id=payment,
                    pledging_id=Pledging.objects.get(id=pledge_id),
                    amount=float(request.POST.getlist('amount')[i]),
                )
            return redirect('inform_payment', payment.id)
    return render(request, template_name='view_payment.html', context=context)

@login_required
def inform_payment(request, payment_id):
    context = {'type': 'inform', 'detail': list(), 'payment': Online.objects.get(id=payment_id)}
    if request.user.is_staff:
        pass
    else:
        customer = Customer.objects.get(user_acc=request.user)
    payment = Online.objects.get(id=payment_id)
    context['payment_id'] = payment_id
    for transaction in Transaction.objects.filter(payment_id=payment):
        pledging = transaction.pledging_id
        balance = pledging.pledge_balance
        amount = transaction.amount
        month = amount/(balance*RATE)
        context['detail'] += [{
            'pledge_id': pledging.id,
            'gold': Gold.objects.filter(pledging_id=pledging),
            'balance': balance,
            'amount': amount,
            'month': month,
        }]
    if request.method == 'POST' and 'picture' in request.FILES:
        # save image
        payment.picture = request.FILES['picture']
        payment.save()
        return redirect('inform_payment', payment_id)
    return render(request, template_name='view_payment.html', context=context)

@login_required
@permission_required('payment.change_payment')
def approve_payment(request, payment_id):
    payment = Online.objects.get(id=payment_id)
    payment.user_id = request.user
    payment.status = Status.approve
    payment.save()
    for transaction in Transaction.objects.filter(payment_id=payment):
        create_recontract_trans(transaction, request.user)
    return redirect('inform_payment', payment_id)

@login_required
@permission_required('payment.change_payment')
def reject_payment(request, payment_id):
    payment = Online.objects.get(id=payment_id)
    payment.status = Status.reject
    payment.save()
    return redirect('inform_payment', payment_id)

@login_required
@permission_required('transaction.add_transaction')
def add_transaction(request, pled_id):
    context = {'pledging': Pledging.objects.get(id=pled_id)}
    context['interest'] = context['pledging'].pledge_balance*RATE
    context['redeem'] = redeemed_price(context['pledging'])
    context['msg'] = ""
    context['result'] = 0
    if 'amount' not in context:
        context['amount'] = context['interest']
    if request.method == 'POST':
        transaction = Transaction.objects.create(
                pledging_id=context['pledging'],
                amount=float(request.POST.get('amount')),
                trantype=int(request.POST.get('trantype')),
            )
        if transaction.trantype == 0:
            # ต่อดอก
            create_recontract_trans(transaction, request.user)
            context['msg'] = 'pass'
            context['text'] = 'ต่อดอกสำเร็จ'
        elif transaction.trantype == 1:
            # ไถ่คืน
            return redirect('detail_redeemed', pled_id)
        elif transaction.trantype == 2:
            # ผ่อนจ่าย
            context['new_pledge_id'] = create_slacken_trans(transaction, request.user,\
                float(request.POST.get('amount')), int(request.POST.get('day')))
            context['msg'] = 'slacken'
            context['result'] = float(request.POST.get('amount'))\
                +(redeemed_price(context['pledging'])-context['pledging'].pledge_balance)
        elif transaction.trantype == 3:
            # เอาเพิ่ม
            context['new_pledge_id'] = create_getmore_trans(transaction, request.user,\
                float(request.POST.get('amount')), int(request.POST.get('day')))
            context['msg'] = 'getmore'
            context['result'] = float(request.POST.get('amount'))\
                -(redeemed_price(context['pledging'])-context['pledging'].pledge_balance)
    return render(request, 'add_transaction.html', context=context)

@login_required
def detail_redeemed(request, pled_id):
    context = {'pledging': Pledging.objects.get(id=pled_id)}
    if request.method == 'POST':
        redeemed_form = RedeemedForm(request.POST)
        if redeemed_form.is_valid():
            redeemed = redeemed_form.save()
            context['pledging'].type_pledging = 2
            context['pledging'].save()
            log = Log.objects.create(user_id=request.user, detail=1, cus_id=context['pledging'].cus_id)
            context['msg'] = 'pass'
        else:
            context['msg'] = 'not_pass'
    else:
        redeemed_form = RedeemedForm(initial={'pledging_id': context['pledging']})
    context['redeemed_form'] = redeemed_form
    return render(request, 'detail_redeemed.html', context=context)
