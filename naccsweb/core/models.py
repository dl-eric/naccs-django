from django.db import models


# Create your models here.

class hubStats(models.Model):
    matches = models.IntegerField()