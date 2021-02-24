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
    path(
        "customers/<int:pk>/delete/",
        CustomerDeleteView.as_view(),
        name="customer_delete",
    ),
    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/add", AddressEditView.as_view(), name="address_add"),
    path("addresses/<int:pk>/edit/", AddressEditView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/", AddressView.as_view(), name="address"),
    path(
        "addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"
    ),
    path(
        "billing-package/", BillingPackageListView.as_view(), name="billingpackage_list"
    ),
    path(
        "billing-package/add",
        BillingPackageEditView.as_view(),
        name="billingpackage_add",
    ),
    path(
        "billing-package/<int:pk>/edit/",
        BillingPackageEditView.as_view(),
        name="billingpackage_edit",
    ),
    path(
        "billing-package/<int:pk>/", BillingPackageView.as_view(), name="billingpackage"
    ),
    path(
        "billing-package/<int:pk>/delete/",
        BillingPackageDeleteView.as_view(),
        name="billingpackage_delete",
    ),

    path("accounts/", AccountListView.as_view(), name="account_list"),
    path("accounts/add", AccountEditView.as_view(), name="account_add"),
    path("accounts/<int:pk>/edit/", AccountEditView.as_view(), name="account_edit"),
    path("accounts/<int:pk>/", AccountView.as_view(), name="account"),
    path("accounts/<int:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),

    path("equipment/", EquipmentListView.as_view(), name="equipment_list"),
    path("equipment/add", EquipmentEditView.as_view(), name="equipment_add"),
    path("equipment/<int:pk>/edit/", EquipmentEditView.as_view(), name="equipment_edit"),
    path("equipment/<int:pk>/", EquipmentView.as_view(), name="equipment"),
    path("equipment/<int:pk>/delete/", EquipmentDeleteView.as_view(), name="equipment_delete"),

]
