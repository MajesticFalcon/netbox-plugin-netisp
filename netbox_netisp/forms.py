from django import forms
from django.urls import reverse
from utilities.forms import BootstrapMixin, SlugField, DynamicModelChoiceField, APISelect

from .models import *
from .models import AntennaProfile

from django.core.validators import RegexValidator

class CustomerForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "email",
        )

state_validator = RegexValidator(r'\d', message="Only input the 2 character code for your state", inverse_match=1)

class AddressForm(BootstrapMixin, forms.ModelForm):
    state_code = forms.CharField(validators=[state_validator])
    class Meta:
        model = Address
        fields = (
            "street_number",
            "street_ordinance",
            "street_name",
            "street_suffix",
            "city",
            "state_code",
            "zip",
        )


class BillingPackageForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = BillingPackage
        fields = ("name", "price", "download_speed", "upload_speed", "data_cap", "slug")


class CustomerFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering BgpPeering instances."""

    q = forms.CharField(required=False, label="Search")

    first_name = forms.CharField(
        required=False,
        label="First Name",
    )

    last_name = forms.CharField(
        required=False,
        label="Last Name",
    )


    class Meta:
        model = Customer
        fields = []


class AccountForm(BootstrapMixin, forms.ModelForm):

    primary_applicant = DynamicModelChoiceField(
        queryset=Customer.objects.all(),
        required=True,
        display_field='name',
        widget=APISelect(
            api_url='/api/plugins/netbox_netisp/customers/'
        ),
    )
    
    class Meta:
        model = Account
        fields = ("primary_applicant",)


class EquipmentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ("serial", "manufacturer", "device_type")

class AntennaProfileForm( BootstrapMixin, forms.ModelForm):
    return_url = forms.CharField(widget=forms.HiddenInput(), initial="/plugins/netbox_netisp/antenna-profile/")

    class Meta:
        model = AntennaProfile
        fields = ("name", "serial", "manufacturer", "device_type", "azimuth", "beamwidth")

class RadioAccessPointForm(BootstrapMixin, forms.ModelForm):
    return_url = forms.CharField(widget=forms.HiddenInput(), initial="/plugins/netbox_netisp/sector/")

    class Meta:
        model = RadioAccessPoint
        fields = ("name", "manufacturer", "device_type", "frequency", "antenna", "ip_address")

class CustomerPremiseEquipmentForm(BootstrapMixin, forms.ModelForm):
    return_url = forms.CharField(widget=forms.HiddenInput(), initial="/plugins/netbox_netisp/customer-premise-equipment/")
    class Meta:
        model = CustomerPremiseEquipment
        fields = ("ip_address", "manufacturer", "device_type", "serial")

class TicketForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("notes","priority")

class WirelessTicketForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = WirelessTicket
        exclude = ('status', 'type')
        field_order = ['password']

class ServiceForm(BootstrapMixin, forms.ModelForm):
    
    billing_package = forms.ModelChoiceField(queryset=BillingPackage.objects.all())
    account = forms.ModelChoiceField(queryset=Account.objects.all(), disabled = True)
    status = forms.CharField(disabled = True)
    
    address = DynamicModelChoiceField(
        queryset=Address.objects.all(),
        required=True,
        display_field='name',
        widget=APISelect(
            api_url='/api/plugins/netbox_netisp/addresses/'
        ),
    )
    
    
    class Meta:
        model = Service
        fields = ("account", "status", "type", "billing_package", "address")