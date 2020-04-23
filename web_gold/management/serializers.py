from rest_framework import serializers

from .models import Pledging, Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
class ToDoItemSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source='cus_id.first_name')
    last_name = serializers.CharField(max_length=255, source='cus_id.last_name')
    class Meta:
        model = Pledging
        fields = ('id', 'pledge_balanca', 'contract_term', 'pledge_date','expire_date', 'type_pledging', 'first_name', 'last_name')
