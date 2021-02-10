from django.db import models
from extras.models import ChangeLoggedModel

class Customer(ChangeLoggedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
