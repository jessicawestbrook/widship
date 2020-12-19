from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
from django_countries.fields import CountryField
from stdimage import StdImageField, JPEGField



class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("friendship.Friend", blank=True)
    profile_photo = StdImageField(upload_to='images/', null=True, blank=True, variations={'profile_card': {'width': 200, 'height': 200}})
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    fb_locale = models.CharField(max_length=50, null=True, blank=True)
    fb_timezone = models.CharField(max_length=50, null=True, blank=True)
    fb_link = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gps_coords = models.PointField(blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def calculate_age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25  )
    age = property(calculate_age)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()