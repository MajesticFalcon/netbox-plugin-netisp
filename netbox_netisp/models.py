from django.db import models
from extras.models import ChangeLoggedModel
from datetime import datetime

class Customer(ChangeLoggedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def name(self):
        return "{0} {1} {2}".format(self.first_name, self.middle_name, self.last_name)
