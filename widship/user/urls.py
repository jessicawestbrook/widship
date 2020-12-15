from django.urls import path
from django.conf.urls import include, url
from . import views
from .views import(delete_user_view,)


app_name = 'user'

urlpatterns = [
    path('delete', delete_user_view, name='delete_user_view'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('search', views.SearchPage.as_view(), name='search'),
    path('profile_form', views.ProfileFormPage.as_view(), name='profile_form'),
    path('<str:username>', views.ProfileDetailPage.as_view(), name='profile'),
]