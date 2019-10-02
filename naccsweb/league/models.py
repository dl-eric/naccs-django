from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)

class Team(models.Model):
    name = models.CharField(max_length=80, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    roster = models.ManyToManyField(User)