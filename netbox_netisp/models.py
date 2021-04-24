from django.db import models
from netbox.models import ChangeLoggedModel
from datetime import datetime
from django.urls import reverse
from dcim.models import Manufacturer, DeviceType, Interface, Device, Site
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from ipam.fields import IPAddressField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from netbox_netisp.netbox_netisp.models.crm.models import *


class Equipment(ChangeLoggedModel):
    serial = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:equipment", args=[self.pk])

class CustomerPremiseEquipment(Equipment):
    ip_address = IPAddressField()


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



class Attachment(ChangeLoggedModel):
    image = models.ImageField(upload_to='netbox_netisp/attachments/')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:attachment", args=[self.pk])

class ISPDevice(ChangeLoggedModel):
    name = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    uuid = models.CharField(max_length=255)

class ISPActiveDevice(ISPDevice):
    ip_address = IPAddressField(blank=True, null=True, default="")
    type = models.CharField(max_length=255, null=True, blank=True)

class OLT(ISPActiveDevice):
    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:olt", args=[self.pk])
    pass

class GPONSplitter(ISPDevice):
    uplink_type = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    uplink_port = GenericForeignKey('content_type', 'object_id')

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:gponsplitter", args=[self.pk])

    def __str__(self):
        return self.name

    def parent(self):
        if self.content_type.model == 'olt':
            return OLT.objects.get(pk=self.object_id).name
        else:
            return GPONSplitter.objecst.get(pk=self.object_id).name

class ONT(ISPActiveDevice):
    uplink = models.ForeignKey(GPONSplitter, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("plugins:netbox_netisp:olt", args=[self.pk])
