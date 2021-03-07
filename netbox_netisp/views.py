from django.shortcuts import get_object_or_404, render
from django.views import View
from django_tables2 import LazyPaginator, RequestConfig, SingleTableView
from django.shortcuts import redirect
from django.utils import timezone
from utilities.views import GetReturnURLMixin


from .netbox_netisp.views.generic import (
    ObjectListView,
    ObjectEditView,
    ObjectView,
    ObjectDeleteView,
)
from .models import Customer, Address, BillingPackage, Account, Equipment, RadioAccessPoint, CustomerPremiseEquipment,\
    AntennaProfile, Service
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

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, **kwargs)
        current_account = instance
        services = current_account.service_set.all()
        service_table = tables.ServiceTable(services)
        RequestConfig(request, paginate={"per_page": 2}).configure(service_table)
        return render(
            request,
            self.get_template_name(),
            {
                "object": self.instance,
                "service_table": service_table,
                "service_count": len(services),

            },
        )


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

"""Radio Access Point"""
class RadioAccessPointListView(ObjectListView, View):
    queryset = RadioAccessPoint.objects.all()
    table = tables.RadioAccessPointTable

class RadioAccessPointEditView(ObjectEditView, View):
    queryset = RadioAccessPoint.objects.all()
    model_form = forms.RadioAccessPointForm

class RadioAccessPointView(ObjectView):
    queryset = RadioAccessPoint.objects.all()

"""Antenna Profile"""
class AntennaProfileListView(ObjectListView, View):
    queryset = AntennaProfile.objects.all()
    table = tables.AntennaProfileTable

class AntennaProfileEditView(ObjectEditView, View):
    queryset = AntennaProfile.objects.all()
    model_form = forms.AntennaProfileForm

class AntennaProfileView(ObjectView):
    queryset = AntennaProfile.objects.all()

"""Customer Premise Equipment"""
class CustomerPremiseEquipmentListView(ObjectListView, View):
    queryset = CustomerPremiseEquipment.objects.all()
    table = tables.CustomerPremiseEquipmentTable

class CustomerPremiseEquipmentEditView(ObjectEditView, View):
    queryset = CustomerPremiseEquipment.objects.all()
    model_form = forms.CustomerPremiseEquipmentForm

class CustomerPremiseEquipmentView(ObjectView):
    queryset = CustomerPremiseEquipment.objects.all()
