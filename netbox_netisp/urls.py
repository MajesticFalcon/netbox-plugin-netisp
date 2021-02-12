from django.urls import path
from django.http import HttpResponse
from .views import *




urlpatterns = [

    path("", CustomerListView.as_view(), name="customer_list")
]