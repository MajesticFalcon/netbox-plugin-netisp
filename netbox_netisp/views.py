from datetime import date

from django.shortcuts import get_object_or_404, render
from django.views import View
from django_tables2 import LazyPaginator, RequestConfig, SingleTableView
from django.shortcuts import redirect
from django.utils import timezone
from utilities.views import GetReturnURLMixin
from django.urls import reverse

from .netbox_netisp.models.wireless.models import *
from .netbox_netisp.models.crm.models import *

from .netbox_netisp.views.generic import (
    ObjectListView,
    ObjectEditView,
    ObjectView,
    ObjectDeleteView,
)
from .models import *
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
    selected_service = ''
 
    def set_template_name(self, detail_name):
        """generate_template_name(self, 'wireless_service_detail') => netbox_netisp/account/wireless_service_detail.html"""
        self.selected_service_template = "{0}/{1}.html".format(self.template_plugin_prefix, detail_name)


    def action_parser(self, selected_service, action):
        if action == 'place_hold':
            service = Service.objects.get(pk=selected_service)
            service.status = 'On Hold'
            service.save()
            return redirect(service.account)
        elif action == 'remove_hold':
            service = Service.objects.get(pk=selected_service)
            service.status = 'Active'
            service.save()
            return redirect(service.account)

    def pick_selected_service_table(self, selected_service_pk, status='Incomplete'):

        selected_service = None
        selected_service_template = None

        if selected_service_pk is None:
            self.set_template_name('service_detail_placeholder')
            return

        selected_service_parent = Service.objects.get(pk=selected_service_pk)
        if selected_service_parent.type == 'WIRELESS':
            self.selected_service = Service.objects.get(pk=selected_service_pk)
            self.set_template_name('wireless_service_detail')
        elif selected_service_parent.type == 'FIBER' and status=='Complete':
            selected_service = FiberService.objects.get(pk=selected_service_pk)
        else:
            self.set_template_name('service_detail_placeholder')
            return

    def get(self, request, *args, **kwargs):
        # If the user selected a service row while already on the account page
        #    then we will be provided a service_id in the kwargs
        #    we need to pull this service id out before query the db for the account
        #    once we have it, we can check the type and determine which table to query
        #    and provide the correct service detail db to the template.
        #
        selected_service_pk = kwargs.pop('service_id', None)
        action = kwargs.pop('action', None)

        if action:
            self.action_parser(selected_service_pk, action)

        current_account = get_object_or_404(self.queryset, **kwargs)
        services = current_account.service_set.all()
        ticket_table = None



        if selected_service_pk:
            self.pick_selected_service_table(selected_service_pk)
            service_table = tables.ServiceTable(services)
            RequestConfig(request, paginate={"per_page": 2}).configure(service_table)
            ticket_table = tables.WirelessTicketTable(self.selected_service.ticket_set.all())

        elif len(services) > 0:
            self.pick_selected_service_table(services.first().pk)
            service_table = tables.ServiceTable(services)
            RequestConfig(request, paginate={"per_page": 2}).configure(service_table)
            
            #When installing, the wireless/fiber service hasnt been created yet.
            if self.selected_service != '':
                ticket_table = tables.WirelessTicketTable(self.selected_service.ticket_set.all())

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
                "ticket_table": ticket_table,
                "attachments": current_account.attachment_set.all()

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
    queryset = Ticket.objects.select_subclasses()

    def alter_obj(self, obj, request, url_args, url_kwargs):
        if('service_id' in url_kwargs and 'ticket_type' in url_kwargs):
            obj.service = Service.objects.get(pk=url_kwargs['service_id'])
            obj.type = url_kwargs['ticket_type'].capitalize()

        return obj


    ####model_form needs dynamic ticket init###
    ###current mode hardcoded
    def get(self, request, *args, **kwargs):
        self.model_form = forms.WirelessInstallTicketForm
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.model_form = forms.WirelessInstallTicketForm
        return super().post(request, *args,**kwargs)

class TicketView(ObjectView):
    queryset = Ticket.objects.all()

class TicketDeleteView(ObjectDeleteView):
    queryset = Ticket.objects.all()

class WirelessTicketEditView(ObjectEditView, View):
    queryset = WirelessTicket.objects.all()
    model_form = forms.WirelessTicketForm
    template_name = 'netbox_netisp/wirelessticket_edit.html'

    def alter_obj(self, obj, request, url_args, url_kwargs):
        if '_complete' in request.POST:
            obj.status = 'Awaiting Confirmation'
            obj.date_closed = date.today()
            print(obj.date_closed)

        else:
            pass
        return obj

    def get(self, request, *args, **kwargs):
        current_ticket = get_object_or_404(self.queryset, **kwargs)
        if current_ticket.status == 'Complete':
            return redirect(current_ticket)
        elif current_ticket.status == 'Awaiting Confirmation':
            return redirect(current_ticket)
        else:
            return super().get(request, *args, **kwargs)

class WirelessTicketView(ObjectView):
    queryset = WirelessTicket.objects.all()

class WirelessTicketListView(ObjectListView, View):
    queryset = WirelessTicket.objects.filter(status='Active')
    table = tables.WirelessTicketTable

class WirelessTicketListConfirmationsView(ObjectListView, View):
    queryset = WirelessTicket.objects.filter(status='Awaiting Confirmation')
    table = tables.WirelessTicketConfirmationTable
    template_name = 'netbox_netisp/wirelessticket/confirm_list.html'

class WirelessTicketConfirmationView(ObjectEditView, View):
    queryset = WirelessTicket.objects.all()
    model_form = forms.WirelessTicketConfirmationForm
    template_name = 'netbox_netisp/wirelessticket/confirm.html'

    def post(self, request, *args, **kwargs):
        current_ticket = get_object_or_404(self.queryset, **kwargs)
        current_ticket.status = 'Complete'
        current_ticket.save()
        current_service = current_ticket.service
        current_service.status = 'Active'
        current_service.save()
        return redirect(current_ticket)

"""Services"""
class ServiceListView(ObjectListView, View):
    queryset = Service.objects.all()
    table = tables.ServiceTable

class ServiceEditView(ObjectEditView, View):
    queryset = Service.objects.all()
    model_form = forms.ServiceForm

    def create_install_ticket(self, type):
        if type == 'WIRELESS':
            ticket = WirelessTicket()
            ticket.priority = 'Normal'
            ticket.type = 'Install'
            ticket.status = 'Active'
            ticket.service = self.new_obj
            ticket.save()

    def alter_obj(self, obj, request, url_args, url_kwargs):
        obj.account = Account.objects.get(pk=url_kwargs['account_pk'])
        obj.status = "WO Submitted"
        return obj

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.create_install_ticket(type=request.POST.get('type'))
        return redirect(reverse('plugins:netbox_netisp:account_selected', args=[kwargs['account_pk'], self.new_obj.pk]))

"""Attachments"""

class AttachmentListView(ObjectListView, View):
    queryset = Attachment.objects.all()
    table = tables.AttachmentTable

class AttachmentEditView(ObjectEditView, View):
    queryset = Attachment.objects.all()
    model_form = forms.AttachmentForm

    def alter_obj(self, obj, request, url_args, url_kwargs):
        if 'type' in url_kwargs:
            if url_kwargs['type'] == 'account':
                obj.account = Account.objects.get(pk=url_kwargs['id'])
        return obj

class AttachmentView(ObjectView):
    queryset = Attachment.objects.all()

"""OLT"""
class OLTListView(ObjectListView, View):
    queryset = OLT.objects.all()
    table = tables.OLTTable

class OLTEditView(ObjectEditView, View):
    queryset = OLT.objects.all()
    model_form = forms.OLTForm

class OLTView(ObjectView):
    queryset = OLT.objects.all()

    def get(self, request, *args, **kwargs):
        current_olt = get_object_or_404(self.queryset, **kwargs)
        splitters = GPONSplitter.objects.filter(object_id=current_olt.pk)
        splitter_table = tables.GPONSplitterTable(splitters)
        RequestConfig(request, paginate={"per_page": 5}).configure(splitter_table)

        #outer_list=splitters
        #inner_list=nids
        #return a list of nids whose FK corresponds to one of the splitters linked to this OLT
        onts = [nid for splitter in splitters for nid in splitter.ont_set.all()]
        ont_table = tables.ONTTable(onts)
        RequestConfig(request, paginate={"per_page": 25}).configure(ont_table)


        return render(
            request,
            self.get_template_name(),
            {
                "object": current_olt,
                "splitter_table": splitter_table,
                "splitter_count": len(splitters),
                "ont_table": ont_table,
                "ont_count": len(onts),

            },
        )




