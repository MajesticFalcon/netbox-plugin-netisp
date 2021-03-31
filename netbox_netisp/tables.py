
import django_tables2 as tables
from django.urls import reverse
from django_tables2.utils import A  # alias for Accessor


from .models import *

from utilities.tables import (
    BaseTable,
    ButtonsColumn,
    ChoiceFieldColumn,
    TagColumn,
    ToggleColumn
)



class CustomerTable(BaseTable):
    pk = ToggleColumn()

    first_name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Customer
        fields = ("pk", "first_name", "middle_name", "last_name")


class AddressTable(BaseTable):
    pk = ToggleColumn()

    street_number = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Address
        fields = ("pk", "street_number", "street_name", "street_suffix")


class BillingPackageTable(BaseTable):
    pk = ToggleColumn()

    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = BillingPackage
        fields = ("pk", "name", "price", "download_speed", "upload_speed", "data_cap")


class AccountTable(BaseTable):

    pk = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Account
        fields = ("pk", "primary_applicant.name")


class EquipmentTable(BaseTable):

    pk = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Equipment
        fields = ("serial", "manufacturer", "device_type", )

class RadioAccessPointTable(EquipmentTable):

    pk = tables.LinkColumn()
    name = tables.LinkColumn('plugins:netbox_netisp:radioaccesspoint', args=[A("pk")])

    class Meta(BaseTable.Meta):
        model = RadioAccessPoint
        fields = ("antenna", "ip_address")

class AntennaProfileTable(EquipmentTable):
    name = tables.LinkColumn('plugins:netbox_netisp:antennaprofile', args=[A("pk")])

    class Meta(BaseTable.Meta):
        model = AntennaProfile
        fields = ("name",)

class CustomerPremiseEquipmentTable(EquipmentTable):

    pk = tables.LinkColumn('plugins:netbox_netisp:customerpremiseequipment', args=[A("pk")])

    class Meta(BaseTable.Meta):
        model = CustomerPremiseEquipment
        fields = ("ip_address",)

class ServiceTable(BaseTable):
    pk = ToggleColumn()

    clickable = {'td': {'onclick': lambda record: "window.location='{0}'".format(reverse('plugins:netbox_netisp:account_selected',kwargs={'pk': record.account.pk, 'service_id': record.pk}))}}

    speed = tables.Column(
        verbose_name="Speed",
        accessor=A('billing_package__download_speed'),
        linkify=False,
        attrs=clickable
    )

    mrc = tables.Column(
        verbose_name="MRC",
        accessor=A('billing_package__price'),
        linkify=False,
        attrs=clickable
    )

    billing_package = tables.Column(attrs=clickable)
    address = tables.Column(attrs=clickable)

    def render_speed(self, value, record):
        return "↓ {0}mbps / ↑ {1}mbps ".format(value, record.billing_package.upload_speed)

    def render_mrc(self, value):
        return "${0}/month".format(value)

    class Meta(BaseTable.Meta):
        model = Service
        fields = ("pk", "billing_package", "address", "mrc", "speed", "status")


# May not use these in favor of manual panels in template
#    the panel provides a more consistent UI similar to what the techs are used to
class ServiceDetailTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = Service
        fields = ("type", "cpe.ip_address")

class WirelessServiceDetailTable(ServiceDetailTable):
    class Meta(BaseTable.Meta):
        model = WirelessService
        fields = ("sector",)


class TicketTable(BaseTable):
    type = tables.Column(verbose_name="Ticket Type")
    service__type = tables.LinkColumn(verbose_name="Service Type")
    class Meta(BaseTable.Meta):
        model = Ticket
        fields = ("pk", "type", "service", "service__type", "date_opened", "date_closed", "priority", "notes")

class WirelessTicketTable(BaseTable):

    pk = tables.LinkColumn()

    type = tables.Column(verbose_name="Ticket Type")

    class Meta(BaseTable.Meta):
        model = WirelessTicket
        fields = ("pk", "type", "service", "date_opened", "date_closed", "priority", "notes")
