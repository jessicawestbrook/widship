# Generated by Django 3.1.4 on 2020-12-15 20:47

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friendship', '0004_auto_20200408_1844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', stdimage.models.StdImageField(blank=True, null=True, upload_to='media/images/')),
                ('profile_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.TextField(blank=True, max_length=1000, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gps_coords', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('friends', models.ManyToManyField(blank=True, to='friendship.Friend')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
