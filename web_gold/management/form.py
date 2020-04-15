from django import forms
from django.forms import ModelForm
from django.forms.widgets import Input, DateTimeInput

from .models import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'user_id': forms.HiddenInput(),
            'first_name':Input(attrs={'class':'form-control'}),
            'last_name':Input(attrs={'class':'form-control'}),
            'email':Input(attrs={'class':'form-control'}),
            'citizen_id':Input(attrs={'class':'form-control'}),
            'dob':Input(attrs={'class':'form-control','type':'date'}),
        }
        labels = {
            'first_name' : 'ชื่อ',
            'last_name' : 'นามสกุล',
            'email' : 'Email',
            'citizen_id' : 'รหัสประชาชน',
            'dob' : 'วันเกิด'}
    def clean(self):
       citizen_id = self.cleaned_data.get('citizen_id')
       if not citizen_id.isdigit():
             self.add_error('citizen_id',"Citizen id Digit Only!!")
       return self.cleaned_data