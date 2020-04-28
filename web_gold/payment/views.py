from datetime import date, datetime, timedelta

from django.shortcuts import redirect, render

from management.models import Customer, Gold, Pledging, PledgingType, Log
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

def redeem_price(pledging):
    """ return redeem price """
    balance = pledging.pledge_balance
    days = min((datetime.now().date() - lasted_date(pledging)).days, 1)
    return balance + balance*(math.ceil(days/10)/3*(1+(days>10)+(days>20)))/100

def redeem_pledging(pledging):
    pass

# Create your views here.

def payment(request):
    if request.user.is_staff:
        context = {'payment': Online.objects.all().order_by('-pk')}
    else:
        customer = Customer.objects.get(user_acc=request.user)
        context = {'payment': Online.objects.filter(cus_id=customer).order_by('-pk')}
    return render(request, template_name='payment.html', context=context)

def select_pledging(request):
    context = {}
    customer = Customer.objects.get(user_acc=request.user)
    context['pledging'] = Pledging.objects.filter(cus_id=customer).filter(type_pledging=PledgingType.in_contract)
    context['gold'] = {p.id: Gold.objects.filter(pledging_id=p) for p in context['pledging']}
    if request.method == 'POST':
        # go to detail_payment
        if request.POST.getlist('selected'):
            request.session['selected'] = request.POST.getlist('selected')
            return redirect('detail_payment')
        # alert 'no selected pledgings'
    return render(request, template_name='select_pledging.html', context=context)

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

def approve_payment(request, payment_id):
    payment = Online.objects.get(id=payment_id)
    payment.user_id = request.user
    payment.status = Status.approve
    payment.save()
    for transaction in Transaction.objects.filter(payment_id=payment):
        pledging = transaction.pledging_id
        increase_days = transaction.amount/(pledging.pledge_balance*RATE)*30
        # update contract_term and expire_date
        pledging.contract_term += increase_days
        pledging.expire_date = pledging.expire_date+timedelta(days=increase_days)
        pledging.save()
        # create recontract
        recontract = Recontract.objects.create(
            pledging_id=pledging,
            transaction_id=transaction, 
            start_date=lasted_date(pledging)+timedelta(days=increase_days),
        )
        # log
        log = Log.objects.create(
            user_id=request.user,
            detail=0,
            cus_id=pledging.cus_id,
        )
    return redirect('inform_payment', payment_id)

def reject_payment(request, payment_id):
    payment = Online.objects.get(id=payment_id)
    payment.status = Status.reject
    payment.save()
    return redirect('inform_payment', payment_id)

def add_transaction(request, pled_id):
    context = {'pledging': Pledging.objects.get(id=pled_id)}
    context['interest'] = context['pledging'].pledge_balance*RATE
    context['redeem'] = redeem_price(context['pledging'])
    if request.method == 'POST':
        pass
    else:
        context['amount'] = context['interest']
    return render(request, 'add_transaction.html', context=context)
