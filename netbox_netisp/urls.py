from django.urls import path
from django.http import HttpResponse

from .views import *
from .netbox_netisp.views.generic import HomeView

app_name = "netbox_netisp"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("customers/add", CustomerEditView.as_view(), name="customer_add"),
    path("customers/<int:pk>/edit/", CustomerEditView.as_view(), name="customer_edit"),
    path("customers/<int:pk>/", CustomerView.as_view(), name="customer"),
    path("customers/<int:pk>/delete/", CustomerDeleteView.as_view(), name="customer_delete"),

    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/add", AddressEditView.as_view(), name="address_add"),
    path("addresses/<int:pk>/edit/", AddressEditView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/", AddressView.as_view(), name="address"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),

    path("billing-package/", BillingPackageListView.as_view(), name="billingpackage_list"),
    path("billing-package/add", BillingPackageEditView.as_view(), name="billingpackage_add"),
    path("billing-package/<int:pk>/edit/", BillingPackageEditView.as_view(), name="billingpackage_edit"),
    path("billing-package/<int:pk>/", BillingPackageView.as_view(), name="billingpackage"),
    path("billing-package/<int:pk>/delete/", BillingPackageDeleteView.as_view(), name="billingpackage_delete"),

    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/add", AccountEditView.as_view(), name="account_add"),
    path("accounts/<int:customer_pk>/add", AccountEditView.as_view(), name="account_add"),
    path("accounts/<int:pk>/edit/", AccountEditView.as_view(), name="account_edit"),
    path("accounts/<int:pk>/", AccountView.as_view(), name="account"),
    path("accounts/<int:pk>/<int:service_id>", AccountView.as_view(), name="account_selected"),
    path("accounts/<int:pk>/<str:action>", AccountView.as_view(), name="account_update"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),

    path("equipment/", EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/add", EquipmentEditView.as_view(), name="equipment_add"),
    path("equipment/<int:pk>/edit/", EquipmentEditView.as_view(), name="equipment_edit"),
    path("equipment/<int:pk>/", EquipmentView.as_view(), name="equipment"),
    path("equipment/<int:pk>/delete/", EquipmentDeleteView.as_view(), name="equipment_delete"),

    path("sector/<int:pk>/", RadioAccessPointView.as_view(), name="radioaccesspoint"),

    path("sector/", RadioAccessPointListView.as_view(), name="radioaccesspoint_list"),
    path("sector/add", RadioAccessPointEditView.as_view(), name="radioaccesspoint_add"),
    path("sector/<int:pk>/edit", RadioAccessPointEditView.as_view(), name="radioaccesspoint_edit"),

    path("antenna-profile/", AntennaProfileListView.as_view(), name="antennaprofile_list"),
    path("antenna-profile/add", AntennaProfileEditView.as_view(), name="antennaprofile_add"),
    path("antenna-profile/<int:pk>/edit/", AntennaProfileEditView.as_view(), name="antennaprofile_edit"),
    path("antenna-profile/<int:pk>/", AntennaProfileView.as_view(), name="antennaprofile"),

    path("customer-premise-equipment/", CustomerPremiseEquipmentListView.as_view(), name="customerpremiseequipment_list"),
    path("customer-premise-equipment/add", CustomerPremiseEquipmentEditView.as_view(), name="customerpremiseequipment_add"),
    path("customer-premise-equipment/<int:pk>/edit/", CustomerPremiseEquipmentEditView.as_view(), name="customerpremiseequipment_edit"),
    path("customer-premise-equipment/<int:pk>/", CustomerPremiseEquipmentView.as_view(), name="customerpremiseequipment"),

    path("tickets/", TicketListView.as_view(), name="ticket_list"),
    path("ticket/add/", TicketEditView.as_view(), name="ticket_add"),
    path("ticket/add/<int:service_id>/<str:ticket_type>/", TicketEditView.as_view(), name="ticket_add"),
    path("ticket/<int:pk>/edit/", TicketEditView.as_view(), name="ticket_edit"),
    path("ticket/<int:pk>", TicketView.as_view(), name="ticket"),
    path("ticket/<int:pk>/delete", TicketDeleteView.as_view(), name="ticket_delete"),

    path("wireless-tickets/", WirelessTicketListView.as_view(), name="wirelessticket_list"),
    path("wireless-ticket/add/", WirelessTicketEditView.as_view(), name="wirelessticket_add"),
    path("wireless-ticket/<int:pk>/edit/", WirelessTicketEditView.as_view(), name="wirelessticket_edit"),
    path("wireless-ticket/<int:pk>", WirelessTicketView.as_view(), name="wirelessticket"),
    
    path("wireless-ticket/confirmations", WirelessTicketListConfirmationsView.as_view(), name="wirelessticket_confirm_list"),
    path("wireless-ticket/<int:pk>/confirmation", WirelessTicketConfirmationView.as_view(), name="wirelessticket_confirm"),
    
    path("service/", ServiceListView.as_view(), name="service_list"),
    path("service/add/<int:account_pk>", ServiceEditView.as_view(), name="service_add"),

]

