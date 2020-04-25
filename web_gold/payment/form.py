from django import forms
from django.forms import ModelForm
from django.forms.widgets import Input, HiddenInput, DateTimeInput, FileInput, Select

# from pkg_resources import require
# from django.contrib.auth.forms import UserCreationForm
# from .models import Customer, Gold, Pledging
# from django.contrib.auth.models import User
# from django.db.models import Q

from .models import Online, Transaction
from management.models import Pledging

class OnlinePaymentForm(ModelForm):
    picture = forms.FileField(label='รูปหลักฐาน')
    class Meta:
        model = Online
        fields = ['first_name', 'last_name', 'total_amount', 'picture']
        widgets = {
            'first_name': Input(attrs={'class': 'form-control'}),
            'last_name': Input(attrs={'class': 'form-control'}),
            'total_amount': Input(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': 'ชื่อ',
            'last_name': 'นามสกุล',
            'total_amount': 'จำนวนเงินรวม',
        }
    def clean(self):
        return self.cleaned_data

class TransactionForm(ModelForm):
    payment_id = forms.IntegerField(widget=HiddenInput, required=False)
    amount = forms.IntegerField(widget=Input(attrs={'class': 'form-control col mx-5 mb-1'}), label='จำนวนเงิน', )
    class Meta:
        model = Transaction
        exclude = ['trantype']
    def __init__(self, cus_id=None, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        if cus_id:
            self.fields['pledging_id'] = forms.ModelChoiceField(
                widget=forms.Select(attrs={'class': 'form-control col mx-5 mb-1'}),
                label='รายการจำนำ',
                empty_label=None,
                queryset=Pledging.objects.filter(cus_id=cus_id),
            )