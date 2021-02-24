from django.contrib import admin
from .models import Customer, Address, BillingPackage


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_number", "street_ordinance", "street_name")


@admin.register(BillingPackage)
class BillingPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "download_speed", "upload_speed", "data_cap")

    """ defining viewable fields, list display """
