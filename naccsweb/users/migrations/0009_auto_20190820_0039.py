# Generated by Django 2.2.4 on 2019-08-20 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='college',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
