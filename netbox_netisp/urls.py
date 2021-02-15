from django.urls import path
from django.http import HttpResponse

from .views import *
from .netbox_netisp.views.generic import HomeView

app_name = 'netbox_netisp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("customers/add", CustomerEditView.as_view(), name="customer_add"),
    path("customers/<slug:slug>/edit/", CustomerEditView.as_view(), name="customer_edit"),
    path('customers/<slug:slug>/', CustomerView.as_view(), name='customer'),

    path("addresses/", AddressListView.as_view(), name="address_list"),
    path("addresses/<int:pk>/edit/", AddressEditView.as_view(), name="address_edit"),

]