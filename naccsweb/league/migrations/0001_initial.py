# Generated by Django 2.2.4 on 2019-10-22 23:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import league.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('fee', models.IntegerField(default=0)),
                ('sub_fee', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email_domain', models.CharField(blank=True, max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
                ('is_active', models.BooleanField(default=False)),
                ('abbreviation', models.CharField(max_length=12)),
                ('picture', models.ImageField(null=True, upload_to=league.models.get_file_path)),
                ('rank', models.PositiveIntegerField(blank=True, default=0)),
                ('main_color', models.CharField(blank=True, max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('is_active', models.BooleanField(default=False)),
                ('join_password', models.CharField(blank=True, max_length=64)),
                ('captain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='captain', to=settings.AUTH_USER_MODEL)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.Division')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='league.School')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, max_length=12)),
                ('amount_paid', models.IntegerField(default=0)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='league.Team')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('paymentid', models.CharField(blank=True, max_length=50)),
                ('payerid', models.CharField(blank=True, max_length=25)),
                ('date', models.CharField(blank=True, default=datetime.datetime(2019, 10, 22, 23, 34, 42, 260225), max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
