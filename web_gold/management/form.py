from django import forms
from django.forms import ModelForm, Select
from django.forms.widgets import DateTimeInput, HiddenInput, Input
from pkg_resources import require

from .models import Customer, Gold, Pledging


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

class PledgingForm(ModelForm):
    class Meta:
        model = Pledging
        fields = '__all__'
        widgets = {
            'user_id': forms.HiddenInput(),
            'type_pledging': forms.HiddenInput(),
            'cus_id':Input(attrs={'class':'form-control'}),
            'pledge_balanca':Input(attrs={'class':'form-control'}),
            'contract_term':Input(attrs={'class':'form-control'}),
            'expire_date':Input(attrs={'class':'form-control','type':'date'}),
            'dob':Input(attrs={'class':'form-control','type':'date'}),
        }
        labels = {
            'cus_id' : 'รหัสลูกค้า',
            'pledge_balanca' : 'ยอดจำนำ',
            'contract_term' : 'เวลาสัญญา ( เป็นวัน )',
            'pledge_date' : 'วันเริ่มทำสัญญา',
            'expire_date' : 'วันหมดสัญญา'}
        
class GoldForm(ModelForm):
    gold_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta:
        
        model = Gold
        fields = ['weight', 'goldtype']
        widgets = {
            
            'weight':Input(attrs={'class':'form-control'}),
            'goldtype':Select(attrs={'class':'form-control mb-5'}),
            
        }
        labels = {
            'weight' : 'น้ำหนักทอง',
            'goldtype' : 'ประเภททอง'
            }
