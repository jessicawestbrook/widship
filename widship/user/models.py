from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.apps import apps




class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("friendship.Friend", null=True, blank=True)
    profile_photo = models.ImageField(upload_to='images/', null=True, blank=True)
    profile_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gps_coords = models.PointField(blank=True, null=True)
    partner_profile_photo = models.ImageField(upload_to='images/', null=True, blank=True)
    partner_name = models.CharField(max_length=100, null=True, blank=True)
    partner_bio = models.TextField(max_length=1000, null=True, blank=True)
    anniversary = models.DateField(null=True, blank=True)
    partner_birth_date = models.DateField(null=True, blank=True)
    years_together = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user + ": " + str(self.profile_photo)

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