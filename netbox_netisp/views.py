

from django.shortcuts import get_object_or_404, render
from django.views import View
from django_tables2 import LazyPaginator, RequestConfig, SingleTableView
from django.shortcuts import redirect
from django.utils import timezone

from .netbox_netisp.views.generic import ObjectListView, ObjectEditView, ObjectView
from .models import  Customer
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
