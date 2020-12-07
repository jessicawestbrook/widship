from django.urls import path
from django.conf.urls import include, url
from requests.api import request
from . import views



urlpatterns = [
    path('update_profile', views.update_profile, name='update_profile'),
    path('search', views.SearchPage.as_view(), name='search'),
    path('name_search', views.NameSearchPage.as_view(), name='name_search'),
    path('profile_form', views.ProfileFormPage.as_view(), name='profile_form'),
    path('profile', views.ProfilePage.as_view(), name='profile'),
    path('profile/<str:username>', views.ProfileDetailPage.as_view(), name='profile-detail'),
]