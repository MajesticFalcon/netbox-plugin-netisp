from django.db import models
from netbox.models import ChangeLoggedModel
from datetime import datetime
from django.urls import reverse
from dcim.models import Manufacturer, DeviceType, Interface, Device
from ipam.fields import IPAddressField
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager


class Customer(ChangeLoggedModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name()

    def name(self):
        return "{0} {1} {2}".format(self.first_name, self.middle_name, self.last_name)

    def age(self):
        return datetime.now().year - self.birthdate.year

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:customer", args=[self.pk])

class BillingPackage(ChangeLoggedModel):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    download_speed = models.IntegerField()
    upload_speed = models.IntegerField()
    data_cap = models.IntegerField()
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:billingpackage", args=[self.pk])

    def __str__(self):
        return "{0}".format(self.name)



class Address(ChangeLoggedModel):
    street_number = models.IntegerField()
    street_ordinance = models.CharField(max_length=1)
    street_name = models.CharField(max_length=255)
    street_suffix = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_code = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:address", args=[self.pk])

    def name(self):
        if self.street_ordinance:
            return "{0} {1}. {2} {3}".format(
                self.street_number,
                self.street_ordinance.capitalize(),
                self.street_name.capitalize(),
                self.street_suffix.capitalize(),
            )
        else:
            return "{0} {1} {2}".format(
                self.street_number,
                self.street_name.capitalize(),
                self.street_suffix.capitalize(),
            )

    def __str__(self):
        return self.name()

class Account(ChangeLoggedModel):
    primary_applicant = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:account", args=[self.pk])

    def __str__(self):
        return "{0}".format(self.primary_applicant.name())
