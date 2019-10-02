# Generated by Django 2.2.4 on 2019-10-02 21:57

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_collegiate_hub_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=users.models.get_file_path),
        ),
    ]
