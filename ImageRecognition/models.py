from django.db import models

# Create your models here.
from django.db import models


class Status(models.Model):
    id = models.IntegerField(default='0', primary_key=True)
    status = models.BooleanField(default='True')
