from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "profile_pics/" + filename

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    verified_student = models.BooleanField(default=False)
    college = models.CharField(max_length=80, blank=True)
    college_email = models.EmailField(blank=True)
    # TODO: Link to school db
    grad_date = models.DateField(null=True, blank=True)
    discord = models.CharField(max_length=32, blank=True)
    faceit = models.CharField(max_length=32, blank=True)
    collegiate_hub_invite = models.CharField(max_length=8, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    picture = models.ImageField(upload_to=get_file_path, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()