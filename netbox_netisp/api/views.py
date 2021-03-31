from rest_framework.viewsets import ModelViewSet
from netbox_netisp.models import Customer, Address
from .serializers import CustomerSerializer, AddressSerializer
from netbox_netisp.filters import AddressFilterSet
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_class = AddressFilterSet