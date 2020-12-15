from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

app_name = 'friends'

urlpatterns = [
    path('add/<str:username>', views.create_friend_request, name='add'),
    path('requests', views.FriendRequestsPage, name='list_requests'),
    path('accept_request', views.accept_friend_request, name='accept_request'),
    path('reject_request', views.reject_friend_request, name='reject_request'),
    path('unfriend/<str:username>', views.unfriend, name='unfriend'),
    path('', views.FriendsPage.as_view(), name='friends'),
    path('<str:username>', views.FriendPage.as_view(), name='friend'),
]