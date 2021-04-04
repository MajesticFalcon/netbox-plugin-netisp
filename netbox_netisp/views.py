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
    AntennaProfile, Service, WirelessService, FiberService, Ticket

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

    def get(self, request, *args, **kwargs):
        current_address = get_object_or_404(self.queryset, **kwargs)
        associated_services = Service.objects.filter(address=current_address)
        service_table = tables.ServiceTable(associated_services)
        return render(
            request,
            self.get_template_name(),
            {
                "object": current_address,
                **({"service_table": service_table} if service_table else {}),

            },
        )

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
    def get(self, request, *args, **kwargs):
        if "customer_pk" in kwargs:
            account = Account()
            customer = Customer.objects.get(pk=kwargs["customer_pk"])
            account.primary_applicant = customer
            account.save()
            return redirect(account)
        else:
            return super().get(request, *args, **kwargs)

class AccountView(ObjectView):
    queryset = Account.objects.all()
    template_plugin_prefix = 'netbox_netisp/account/'

    def set_template_name(self, detail_name):
        """generate_template_name(self, 'wireless_service_detail') => netbox_netisp/account/wireless_service_detail.html"""
        self.selected_service_template = "{0}/{1}.html".format(self.template_plugin_prefix, detail_name)

    def pick_selected_service_table(self, selected_service_pk):

        selected_service = None
        selected_service_template = None

        if selected_service_pk is None:
            self.set_template_name('service_detail_placeholder')
            return

        selected_service_parent = Service.objects.get(pk=selected_service_pk)
        if selected_service_parent.type == 'WIRELESS':
            self.selected_service = WirelessService.objects.get(pk=selected_service_pk)
            self.set_template_name('wireless_service_detail')
        else:
            selected_service = FiberService.objects.get(pk=selected_service_pk)

    def get(self, request, *args, **kwargs):
        # If the user selected a service row while already on the account page
        #    then we will be provided a service_id in the kwargs
        #    we need to pull this service id out before query the db for the account
        #    once we have it, we can check the type and determine which table to query
        #    and provide the correct service detail db to the template.
        #
        selected_service_pk = kwargs.pop('service_id', None)
        action = kwargs.pop('action', None)

        ####### Adding section to provide a more complete MVP for users #######
        if action == 'add_service':
            service_error = "ERROR: This feature has not yet been implemented"
        else:
            service_error = None

        if action == 'place_hold' or action == 'disconnect':
            service_detail_error = "ERROR: This feature has not yet been implemented"
        else:
            service_detail_error = None

        ####### END MVP SECTION #######

        current_account = get_object_or_404(self.queryset, **kwargs)
        services = current_account.service_set.all()
        ticket_table = None

        if selected_service_pk:
            self.pick_selected_service_table(selected_service_pk)
            service_table = tables.ServiceTable(services)
            RequestConfig(request, paginate={"per_page": 2}).configure(service_table)
            ticket_table = tables.TicketTable(self.selected_service.ticket_set.all())

        elif len(services) > 0:
            self.pick_selected_service_table(services.first().pk)
            service_table = tables.ServiceTable(services)
            RequestConfig(request, paginate={"per_page": 2}).configure(service_table)
            ticket_table = tables.TicketTable(self.selected_service.ticket_set.all())

        else:
            self.pick_selected_service_table(None)
            service_table = None

        return render(
            request,
            self.get_template_name(),
            {
                "object": current_account,
                **({ "service_table": service_table } if service_table else {} ),
                "service_count": len(services),
                **({ "selected_service": self.selected_service } if 'selected_service' in dir(self) else {} ),
                "selected_service_template": self.selected_service_template,
                **({ "service_error": service_error } if service_error else {}),
                **({ "service_detail_error": service_detail_error } if service_detail_error else {}),
                "ticket_table": ticket_table

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

"""Tickets"""

class TicketListView(ObjectListView, View):
    queryset = Ticket.objects.all()
    table = tables.TicketTable

class TicketEditView(ObjectEditView, View):
    queryset = Ticket.objects.all()
    model_form = forms.TicketForm

    def alter_obj(self, obj, request, url_args, url_kwargs):
        if('service_id' in url_kwargs and 'ticket_type' in url_kwargs):
            obj.service = Service.objects.get(pk=url_kwargs['service_id'])
            obj.type = url_kwargs['ticket_type'].capitalize()

        return obj

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TicketView(ObjectView):
    queryset = Ticket.objects.all()

class TicketDeleteView(ObjectDeleteView):
    queryset = Ticket.objects.all()