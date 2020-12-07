from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static


urlpatterns = [
    path('', views.FriendsPage.as_view(), name='friends'),
    path('<str:username>', views.FriendPage.as_view(), name='friend'),
]