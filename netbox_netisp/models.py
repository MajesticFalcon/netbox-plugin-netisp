from django.db import models
from extras.models import ChangeLoggedModel
from datetime import datetime
from django.urls import reverse

class Customer(ChangeLoggedModel):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateTimeField(blank = True, null = True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True)
        

    def name(self):
        return "{0} {1} {2}".format(self.first_name, self.middle_name, self.last_name)
    def age(self):
        return datetime.now().year - self.birthdate.year
    def get_absolute_url(self):
        return reverse('plugins:netbox_netisp:customer', args=[self.pk])

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
        return reverse('plugins:netbox_netisp:address', args=[self.pk])

    def __str__(self):
        if self.street_ordinance:
            return "{0} {1}. {2} {3}, {4} {5}, {6}".format(self.street_number, self.street_ordinance, self.street_name, self.street_suffix, self.city, self.state_code, self.zip   )
        else:
            return "{0} {1} {2}, {3} {4}, {5}".format(self.street_number, self.street_name, self.street_suffix, self.city, self.state_code, self.zip)
