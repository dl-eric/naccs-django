from django.contrib import admin

from .models import HighSchoolFormModel, GraduateFormModel

# Register your models here.
admin.site.register(HighSchoolFormModel)
admin.site.register(GraduateFormModel)