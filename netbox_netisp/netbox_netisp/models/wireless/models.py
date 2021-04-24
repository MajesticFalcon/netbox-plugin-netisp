from django.db import models
from netbox_netisp.models import Ticket, Equipment, Service
from django.urls import reverse
from dcim.models import Device
from ipam.fields import IPAddressField

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

class WirelessService(Service):
    sector = models.ForeignKey(RadioAccessPoint, on_delete=models.PROTECT)
