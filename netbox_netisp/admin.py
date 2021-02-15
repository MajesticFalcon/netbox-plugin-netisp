from django.contrib import admin
from .models import Customer, Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street_number",
        "street_ordinance",
        "street_name")

