from django import forms
from django.forms import ModelForm
from .models import Profile, User


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user','profile_photo','profile_name','bio','city','state','gender',
        'birth_date','partner_name','partner_bio','partner_profile_photo','years_together',
        'anniversary','partner_birth_date')

class NameSearchForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'profile_name')