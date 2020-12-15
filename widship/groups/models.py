from django.contrib.gis.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
from django_countries.fields import CountryField
from stdimage import StdImageField, JPEGField
from django.template.defaultfilters import slugify
from django.urls import reverse



class Group(models.Model):
    id = models.SlugField(max_length=255, blank=True, default='', unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    member_list = models.ManyToManyField(User)
    creator_username = models.CharField(max_length=50)
    profile_photo = StdImageField(upload_to='images/groups/', null=True, blank=True, variations={'profile_card': {'width': 200, 'height': 200}})
    description = models.TextField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    gps_coords = models.PointField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.profile_photo)
    class Meta:
        ordering = ['name',]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('page', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        super(Group, self).save(*args, **kwargs)