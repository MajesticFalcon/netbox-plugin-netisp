
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor


from .models import Customer, Address, BillingPackage, Account, Equipment, RadioAccessPoint, AntennaProfile, CustomerPremiseEquipment
from utilities.tables import (
    BaseTable,
    ButtonsColumn,
    ChoiceFieldColumn,
    TagColumn,
    ToggleColumn,

)



class CustomerTable(BaseTable):
    pk = ToggleColumn()

    first_name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Customer
        fields = ("pk", "first_name", "middle_name", "last_name", "slug")


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
    name = tables.LinkColumn('plugins:netbox_netisp:radioaccesspoint_edit', args=[A("pk")])

    class Meta(BaseTable.Meta):
        model = RadioAccessPoint
        fields = ("antenna",)

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