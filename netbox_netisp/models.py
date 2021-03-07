from django.db import models
from extras.models import ChangeLoggedModel
from datetime import datetime
from django.urls import reverse
from dcim.models import Manufacturer, DeviceType, Interface
from ipam.fields import IPAddressField

class Customer(ChangeLoggedModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name()

    def name(self):
        return "{0} {1} {2}".format(self.first_name, self.middle_name, self.last_name)

    def age(self):
        return datetime.now().year - self.birthdate.year

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:customer", args=[self.pk])


class Address(ChangeLoggedModel):
    street_number = models.IntegerField()
    street_ordinance = models.CharField(max_length=1)
    street_name = models.CharField(max_length=255)
    street_suffix = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_code = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:address", args=[self.pk])

    def __str__(self):
        if self.street_ordinance:
            return "{0} {1}. {2} {3}, {4} {5}, {6}".format(
                self.street_number,
                self.street_ordinance,
                self.street_name,
                self.street_suffix,
                self.city,
                self.state_code,
                self.zip,
            )
        else:
            return "{0} {1} {2}, {3} {4}, {5}".format(
                self.street_number,
                self.street_name,
                self.street_suffix,
                self.city,
                self.state_code,
                self.zip,
            )


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



class Account(ChangeLoggedModel):
    primary_applicant = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:account", args=[self.pk])

    def __str__(self):
        return "{0}".format(self.primary_applicant.name())

class Equipment(ChangeLoggedModel):
    serial = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:equipment", args=[self.pk])

class CustomerPremiseEquipment(Equipment):
    ip_address = IPAddressField()

class AntennaProfile(Equipment):
    azimuth = models.CharField(max_length=30)
    beamwidth = models.IntegerField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return "Profile: {0}".format(self.name)

class RadioAccessPoint(Equipment):
    ANTENNA_FREQUENCY_CHOICES = (
        ("900mhz", "900"),
        ("2.4ghz", "2.4"),
        ("3.5ghz", "3.5"),
        ("5ghz", "5"),
    )

    frequency = models.CharField(max_length=30, choices=ANTENNA_FREQUENCY_CHOICES)
    name = models.CharField(max_length=30)
    antenna = models.ForeignKey(AntennaProfile, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:radioaccesspoint", args=[self.pk])

    def __str__(self):
        return "{0}".format(self.name)


"""Service model"""
class Service(ChangeLoggedModel):
    SERVICE_CHOICES = (
        ("FIBER", "FIBER"),
        ("WIRELESS", "WIRELESS")
    )

    SERVICE_STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("WO Submitted", "WO Submitted"),
    )

    type = models.CharField(choices=SERVICE_CHOICES, max_length=30)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    billing_package = models.ForeignKey(BillingPackage, on_delete=models.PROTECT)
    cpe = models.ForeignKey(CustomerPremiseEquipment, on_delete=models.PROTECT)
    #status = models.CharField(choices=SERVICE_STATUS_CHOICES, max_length=30)

class WirelessService(Service):
    sector = models.ForeignKey(RadioAccessPoint, on_delete=models.PROTECT)

class FiberService(Service):
    interface = models.ForeignKey(Interface, on_delete=models.PROTECT)

