from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static



app_name = 'messaging'

urlpatterns = [
]