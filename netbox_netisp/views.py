

from django.shortcuts import get_object_or_404, render
from django.views import View
from django_tables2 import LazyPaginator, RequestConfig, SingleTableView
from django.shortcuts import redirect
from django.utils import timezone

from .netbox_netisp.views.generic import ObjectListView, ObjectEditView, ObjectView
from .models import  Customer, Address
from django.views.generic.edit import CreateView, UpdateView
from netbox.views import generic
from . import tables
from . import filters
from . import forms

class CustomerListView(ObjectListView, View):
    queryset = Customer.objects.all()
    table = tables.CustomerTable
    filterset = filters.CustomerFilterSet
    filterset_form = forms.CustomerFilterForm

class CustomerEditView(ObjectEditView, View):
    queryset = Customer.objects.all()
    model_form = forms.CustomerForm

class CustomerView(ObjectView):
    queryset = Customer.objects.all()



"""Address"""
class AddressListView(ObjectListView, View):
    queryset = Address.objects.all()
    table = tables.AddressTable

class AddressEditView(ObjectEditView, View):
    queryset = Address.objects.all()
    model_form = forms.AddressForm

class AddressView(ObjectView):
    queryset = Address.objects.all()
