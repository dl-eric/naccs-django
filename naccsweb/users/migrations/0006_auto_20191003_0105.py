# Generated by Django 2.2.4 on 2019-10-03 01:05

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_merge_20191002_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.get_file_path),
        ),
    ]
