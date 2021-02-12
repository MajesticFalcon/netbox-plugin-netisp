import django_tables2 as tables

from .models import Customer
from utilities.tables import BaseTable, ButtonsColumn, ChoiceFieldColumn, TagColumn, ToggleColumn
class CustomerTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = Customer
        fields = ( 'pk', 'first_name', 'middle_name', 'last_name')