from django import forms
from django.forms import ModelForm, Select
from django.forms.widgets import DateTimeInput, HiddenInput, Input
from pkg_resources import require
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Gold, Pledging
from django.contrib.auth.models import User
from django.db.models import Q
class CustomerForm(ModelForm):
    cus_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Customer
        exclude = {
            'user_acc',
        }
        widgets = {
            'user_id': forms.HiddenInput(),
            'first_name':Input(attrs={'class':'shadow form-control'}),
            'last_name':Input(attrs={'class':'shadow form-control'}),
            'email':Input(attrs={'class':'shadow form-control'}),
            'citizen_id':Input(attrs={'class':'form-control shadow '}),
            'dob':Input(attrs={'class':'shadow form-control','type':'date'}),
        }
        labels = {
            'first_name' : 'ชื่อ',
            'last_name' : 'นามสกุล',
            'email' : 'Email',
            'citizen_id' : 'รหัสประชาชน',
            'dob' : 'วันเกิด'}
    def clean(self):
        email = self.cleaned_data.get('email')
        citizen_id = self.cleaned_data.get('citizen_id')
        cus_id = self.cleaned_data.get('cus_id')
        if ((Customer.objects.filter(email=email).exclude(pk=cus_id)).exists()):
            self.add_error('email',"Email exists")
        if not citizen_id.isdigit():
            self.add_error('citizen_id',"Citizen id Digit Only!!") 
        if (Customer.objects.filter(citizen_id=citizen_id).exclude(pk=cus_id)).exists():
            self.add_error('citizen_id',"Citizen id exists")
        return self.cleaned_data


class PledgingForm(ModelForm):
    class Meta:
        model = Pledging
        exclude = ['expire_date']
        widgets = {
            'user_id': forms.HiddenInput(),
            'type_pledging': forms.HiddenInput(),
            'cus_id':Input(attrs={'class':'form-control', 'readonly':'readonly'}),
            'pledge_balance':Input(attrs={'class':'shadow-sm form-control'}),
            'contract_term':Input(attrs={'class':'shadow-sm form-control'}),
            'dob':Input(attrs={'class':'form-control','type':'date'}),
        }
        labels = {
            'cus_id' : 'รหัสลูกค้า',
            'pledge_balance' : 'ยอดจำนำ',
            'contract_term' : 'เวลาสัญญา ( เป็นวัน )',
            'pledge_date' : 'วันเริ่มทำสัญญา',
            'expire_date' : 'วันหมดสัญญา'}
        
class GoldForm(ModelForm):
    gold_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        model = Gold
        fields = ['weight', 'goldtype']
        widgets = {
            'weight':Input(attrs={'class':'shadow-sm form-control'}),
            'goldtype':Select(attrs={'class':'shadow-sm form-control mb-5'}),
        }
        labels = {
            'weight' : 'น้ำหนักทอง',
            'goldtype' : 'ประเภททอง'
            }

class AdminForm(UserCreationForm):
    admin_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    username = forms.CharField(max_length=30, help_text='<span style="color:gray">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>',widget=forms.TextInput(attrs={
        'class':'shadow-sm form-control'
    }))
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
        'class':'shadow-sm form-control'
    }))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
        'class': 'shadow-sm form-control'
    }))
    email = forms.EmailField(max_length=254 ,help_text='<span style="color:gray">Enter a valid email address</span>',widget=forms.TextInput(attrs={
        'class':'shadow-sm form-control',
    }))
    password1 = forms.CharField(label=('Password:'),max_length=254, help_text='<ul style="color:gray"><li>Your password can’t be too similar to your other personal information.<li>Your password must contain at least 8 characters.<li>Your password can’t be a commonly used password.<li>Your password can’t be entirely numeric.</ul>',widget=forms.PasswordInput(attrs={
        'class': 'shadow-sm form-control',
    }))
    
    password2 = forms.CharField(label=('Password confirmation:'),max_length=254, help_text='<span style="color:gray">Enter the same password as before, for verification.</span>',widget=forms.PasswordInput(attrs={
        'class': 'shadow-sm form-control'
    }))
    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       admin_id = self.cleaned_data.get('admin_id')
       if (User.objects.filter(email=email).exclude(pk=admin_id)).exists():
             self.add_error('email',"Email exists")
       if (User.objects.filter(username=username).exclude(pk=admin_id)).exists():
             self.add_error('username',"Username exists")
       return self.cleaned_data

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            'admin_id'
            ]
        labels = {
        "password1": "password",
        "password2":"comfilm"
    }
