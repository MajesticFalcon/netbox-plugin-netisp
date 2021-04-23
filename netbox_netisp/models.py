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
    azimuth = models.IntegerField()
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
    ip_address = IPAddressField(blank=True, null=True, default="")

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
    cpe = models.ForeignKey(CustomerPremiseEquipment, on_delete=models.PROTECT, null=True)
    status = models.CharField(choices=SERVICE_STATUS_CHOICES, max_length=30)

    def __str__(self):
        return "{0} - {1} - {2}".format(self.account.primary_applicant.name(), self.billing_package.name, self.address)

class WirelessService(Service):
    sector = models.ForeignKey(RadioAccessPoint, on_delete=models.PROTECT)

class FiberService(Service):
    interface = models.ForeignKey(Interface, on_delete=models.PROTECT)


"""Employee model"""
class Employee(ChangeLoggedModel):
    EMPLOYEE_PERMISSION_CHOICES = (
        ("Level 1", "Level 1"),
        ("Level 2", "Level 2"),
        ("Level 3", "Level 3"),
    )

    EMPLOYEE_POSITION_CHOICES = (
        ("Communications Field Technician", "CFT"),
        ("Help Desk", "Held Desk"),
        ("Engineer", "Engineer"),
        ("Manager", "Manager"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hire_date = models.DateTimeField()
    permission_level = models.CharField(choices=EMPLOYEE_PERMISSION_CHOICES, max_length=255)
    position = models.CharField(choices=EMPLOYEE_POSITION_CHOICES, max_length=255)


"""Service Ticketing model"""

#Parent class
class Ticket(ChangeLoggedModel):
    TICKET_SERVICE_PRIORITY_CHOICES = (
        ("Normal", "Normal"),
        ("High", "High")
    )

    TICKET_TYPE_CHOICES = (
        ("Repair", "Repair"),
        ("Upgrade", "Upgrade"),
        ("Install", "Install"),
        ("Disconnect", "Disconnect"),
        ("Place Hold", "Place Hold"),
        ("Remove Hold", "Remove Hold")
    )

    TICKET_STATUS_CHOICES = (
        ("Active", "Active"),
        ("Awaiting Confirmation", "Awaiting Confirmation"),
        ("Complete", "Complete")
    )

    TICKET_TECHNICIAN_CHOICES = (
        ("Roger", "Roger Roger"),
        ("Joe", "Joe Dirt"),
        ("Tom", "Tom Riddle")
    )

    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    date_opened = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(choices=TICKET_SERVICE_PRIORITY_CHOICES, max_length=255)
    type = models.CharField(choices=TICKET_TYPE_CHOICES, max_length=255)
    status = models.CharField(choices=TICKET_STATUS_CHOICES, max_length=255)
    notes = models.TextField(max_length=255)
    technician = models.CharField(choices=TICKET_TECHNICIAN_CHOICES, max_length=255)
    objects = InheritanceManager()


class WirelessTicket(Ticket):
    WIRELESS_TICKET_CONCLUSION_CHOICES = (
        ("PASS", "PASS"),
        ("FAIL", "FAIL"),
        ("SPECIAL", "SPECIAL - SEE NOTES (PASS)"),
        ("SPECIAL", "SPECIAL - SEE NOTES (FAIL)")
    )
    rssi = models.IntegerField(null=True)
    local_noise_floor = models.IntegerField(null=True)
    survey_height = models.IntegerField(null=True)
    conclusion = models.CharField(choices=WIRELESS_TICKET_CONCLUSION_CHOICES,max_length=255,null=True)
    cpe = models.ForeignKey(Device, on_delete=models.PROTECT, null=True)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:wirelessticket", args=[self.pk])

class Attachment(ChangeLoggedModel):
    image = models.ImageField(upload_to='netbox_netisp/attachments/')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
