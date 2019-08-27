from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GraduateFormModel(models.Model):
    class Meta:
        verbose_name = "Graduated Student Application"
        verbose_name_plural = "Graduated Student Applications"

    def __str__(self):
        return self.user.profile.nickname

    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    college    = models.CharField(max_length=80, blank=True)
    grad_date  = models.DateField(null=True, blank=True)
    proof      = models.FileField(upload_to="graduate/proof/")
    other      = models.TextField(max_length=500, blank=True)

class HighSchoolFormModel(models.Model):
    class Meta:
        verbose_name = "High School Student Application"
        verbose_name_plural = "High School Student Applications"
    
    def __str__(self):
        return self.user.profile.nickname

    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    highschool = models.CharField(max_length=80, blank=True)
    college    = models.CharField(max_length=80, blank=True)
    grad_date  = models.DateField(null=True, blank=True)
    proof      = models.FileField(upload_to="highschool/proof/")
    other      = models.TextField(max_length=500, blank=True)
