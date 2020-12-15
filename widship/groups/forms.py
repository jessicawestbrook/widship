from django import forms
from django.forms import ModelForm
from .models import User, Group
from django.utils.safestring import mark_safe


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'profile_photo')