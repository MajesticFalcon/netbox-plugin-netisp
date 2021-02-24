from django.shortcuts import get_object_or_404, render
from django.views import View
from django_tables2 import LazyPaginator, RequestConfig, SingleTableView
from django.shortcuts import redirect
from django.utils import timezone


from .netbox_netisp.views.generic import (
    ObjectListView,
    ObjectEditView,
    ObjectView,
    ObjectDeleteView,
)
from .models import Customer, Address, BillingPackage, Account, Equipment
from django.views.generic.edit import CreateView, UpdateView
from netbox.views import generic
from . import tables
from . import filters
from . import forms

"""Customer"""


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


class CustomerDeleteView(ObjectDeleteView):
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


class AddressDeleteView(ObjectDeleteView):
    queryset = Address.objects.all()


"""BillingPackage"""


class BillingPackageListView(ObjectListView, View):
    queryset = BillingPackage.objects.all()
    table = tables.BillingPackageTable


class BillingPackageEditView(ObjectEditView, View):
    queryset = BillingPackage.objects.all()
    model_form = forms.BillingPackageForm


class BillingPackageView(ObjectView):
    queryset = BillingPackage.objects.all()


class BillingPackageDeleteView(ObjectDeleteView):
    queryset = BillingPackage.objects.all()


"""Account"""


class AccountListView(ObjectListView, View):
    queryset = Account.objects.all()
    table = tables.AccountTable


class AccountEditView(ObjectEditView, View):
    queryset = Account.objects.all()
    model_form = forms.AccountForm


class AccountView(ObjectView):
    queryset = Account.objects.all()


class AccountDeleteView(ObjectDeleteView):
    queryset = Account.objects.all()
    selected_service = {}


"""Equipment"""


class EquipmentListView(ObjectListView, View):
    queryset = Equipment.objects.all()
    table = tables.EquipmentTable


class EquipmentEditView(ObjectEditView, View):
    queryset = Equipment.objects.all()
    model_form = forms.EquipmentForm


class EquipmentView(ObjectView):
    queryset = Equipment.objects.all()


class EquipmentDeleteView(ObjectDeleteView):
    queryset = Equipment.objects.all()
    selected_service = {}
