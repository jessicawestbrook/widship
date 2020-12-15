from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

app_name = 'groups'

urlpatterns = [
    path('search', views.GroupSearchPage.as_view(), name='search'),
    path('create', views.GroupCreatePage.as_view(), name='create'),
    path('add/<str:groupname>', views.create_group_add_request, name='add'),
    path('', views.GroupsPage.as_view(), name='groups'),
    path('<str:groupname>', views.GroupPage.as_view(), name='group_page'),
]