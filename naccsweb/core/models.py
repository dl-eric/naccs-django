from django.db import models


# Create your models here.

class HubStats(models.Model):
    matches = models.IntegerField()