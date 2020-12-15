from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

app_name = 'groups'

urlpatterns = [
    path('search', views.GroupSearchPage.as_view(), name='search'),
    path('create', views.GroupFormPage.as_view(), name='create'),
    #path('<str:group_name>/update', views.GroupFormPage.as_view(), name='update'),
    path('<str:id>/add_member', views.create_group_add_request, name='add'),
    path('create_group', views.create_group, name='create_group'),
    path('', views.GroupsPage.as_view(), name='groups'),
    path('<str:id>', views.GroupPage.as_view(), name='group_page'),
]