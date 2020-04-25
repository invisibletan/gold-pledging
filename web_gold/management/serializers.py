from rest_framework import serializers

from .models import Pledging, Customer, Log
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
class PledgingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source='cus_id.first_name')
    last_name = serializers.CharField(max_length=255, source='cus_id.last_name')
    class Meta:
        model = Pledging
        fields = ('id', 'pledge_balance', 'contract_term', 'pledge_date','expire_date', 'type_pledging', 'first_name', 'last_name')

class LogSerializer(serializers.ModelSerializer):
    first_name_cus = serializers.CharField(max_length=255, source='cus_id.first_name')
    last_name_cus = serializers.CharField(max_length=255, source='cus_id.last_name')
    first_name_user = serializers.CharField(max_length=255, source='user_id.first_name')
    last_name_user = serializers.CharField(max_length=255, source='user_id.last_name')
    class Meta:
        model = Log
        fields = ('id', 'datetime', 'detail',  'first_name_cus', 'last_name_cus',  'first_name_user', 'last_name_user')