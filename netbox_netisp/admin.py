from django.contrib import admin
from .models import (
    Customer,
    Address,
    BillingPackage,
    Account,
    Equipment,
    CustomerPremiseEquipment,
    RadioAccessPoint,
    AntennaProfile,
    WirelessService,
    FiberService,
    Ticket,

    )




@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("primary_applicant",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "middle_name", "last_name")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_number", "street_ordinance", "street_name")


@admin.register(BillingPackage)
class BillingPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "download_speed", "upload_speed", "data_cap")


@admin.register(CustomerPremiseEquipment)
class CustomerPremiseEquipmentAdmin(admin.ModelAdmin):
    list_display = ("ip_address",)

@admin.register(RadioAccessPoint)
class RadioAccessPointAdmin(admin.ModelAdmin):
    list_display = ("name","frequency","antenna")

@admin.register(AntennaProfile)
class AntennaProfileAdmin(admin.ModelAdmin):
    list_display = ("azimuth","beamwidth",)

@admin.register(WirelessService)
class AntennaProfileAdmin(admin.ModelAdmin):
    list_display = ("type","account", "address", "billing_package", "cpe", "sector",)

@admin.register(FiberService)
class AntennaProfileAdmin(admin.ModelAdmin):
    list_display = ("type","account", "address", "billing_package", "cpe", "interface",)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("service","date_opened", "date_closed", "priority", "notes",)