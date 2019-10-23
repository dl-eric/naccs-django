from django.db import models
from django.contrib.auth.models import User
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "school_pics/" + filename

class School(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=80)
    email_domain = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    abbreviation = models.CharField(max_length=12)
    picture = models.ImageField(upload_to=get_file_path, null=True)
    rank = models.PositiveIntegerField(blank=True, default=0)
    main_color = models.CharField(max_length=6, blank=True)

class Division(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=32)
    fee = models.FloatField(default=0)
    sub_fee = models.FloatField(default=0)

class Team(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=80)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    captain = models.ForeignKey(User, related_name="captain", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    join_password = models.CharField(max_length=64, blank=True)

class Player(models.Model):
    def __str__(self):
        return self.user.profile.nickname

    role = models.CharField(max_length=12, blank=True)
    amount_paid = models.FloatField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

class Payment(models.Model):
    def __str__(self):
        return self.paymentid
    
    paymentid = models.CharField(max_length=50, blank=True)
    payerid = models.CharField(max_length=25, blank=True, null=True)
    users = models.ManyToManyField(Player)
    date = models.CharField(max_length=50, default=0, blank=True)