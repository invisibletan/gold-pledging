from django.shortcuts import redirect, render
from django.forms import formset_factory

from .form import OnlinePaymentForm, TransactionForm
from .models import PaymentType
from management.models import Customer

# Create your views here.
def payment(request):
    pass

def inform_payment(request):
    context = {}
    customer = Customer.objects.get(user_acc=request.user)
    TransactionFormSet = formset_factory(TransactionForm)
    trans_formset = TransactionFormSet(cus_id=customer)
    if request.method == 'POST':
        payment_form = OnlinePaymentForm(request.POST, request.FILES)
        trans_formset = TransactionFormSet(request.POST)
        if payment_form.is_valid():
            total_amount = 0
            # check sum of amount of transactions are equal to total_amount of payment
            for trans_form in trans_formset:
                print(trans_form)
                if trans_form.is_valid():
                    total_amount += float(trans_form.cleaned_data.get('amount'))
            if total_amount == float(payment_form.cleaned_data.get('total_amount')):
                payment = payment_form.save(commit=False)  
                payment.cus_id = customer
                payment.save()
                return redirect('index')
        context['msg'] = 'error'
    payment_form = OnlinePaymentForm(initial={
        'first_name': customer.first_name,
        'last_name': customer.last_name,
    })
    context['payment_form'] = payment_form
    context['trans_formset'] = trans_formset
    return render(request, template_name='inform_payment.html', context=context)

def verify_payment(request, payment_id):
    pass
