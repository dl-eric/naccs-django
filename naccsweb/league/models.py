from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    is_active = models.BooleanField(default=False, blank=True)

class Team(models.Model):
    name = models.CharField(max_length=80, blank=True)
    division = models.CharField(max_length=32, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    captain = models.CharField(max_length=80, blank=True)
    roster = models.ManyToManyField(User)