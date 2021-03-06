from django import forms
from django.forms import ModelForm
from .models import Profile, User
from django.utils.safestring import mark_safe


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('user','profile_photo','profile_name','bio','city','state','gender','birth_date')