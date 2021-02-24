import django_tables2 as tables

<<<<<<< HEAD
from .models import Customer, Address, BillingPackage, Account
from utilities.tables import BaseTable, ButtonsColumn, ChoiceFieldColumn, TagColumn, ToggleColumn
=======
from .models import Customer, Address, BillingPackage
from utilities.tables import (
    BaseTable,
    ButtonsColumn,
    ChoiceFieldColumn,
    TagColumn,
    ToggleColumn,
)
>>>>>>> 57a258a04d3a9e6bc70540c8bd7b05e4f9a65707


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
        fields = ( 'pk', 'name', 'price', 'download_speed', 'upload_speed', 'data_cap')

class AccountTable(BaseTable):

    pk = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Account
        fields = ( 'pk', 'primary_applicant.name')

