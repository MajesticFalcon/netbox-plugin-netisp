from rest_framework.serializers import ModelSerializer
from netbox_netisp.models import Customer, Address
from rest_framework import serializers

class CustomerSerializer(ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'name')
        
class AddressSerializer(ModelSerializer):
    
    class Meta:
        model = Address
        fields = ('id', 'street_number', 'street_name', 'name')