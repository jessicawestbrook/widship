from django import template
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from friendship.models import Friend, Follow, Block
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User




class FriendsPage(LoginRequiredMixin, ListView):
    Profile = apps.get_model('user', 'Profile')
    model = Friend
    context_object_name = 'friend_list'
    template_name = 'friend_list.html'

    def __init__(self):
        super(FriendsPage, self).__init__()

    def get_context_data(self):
        Profile = apps.get_model('user', 'Profile')
        friend_list = Friend.objects.friends(self.request.user)
        #friend_list = Friend.objects.filter(from_user = self.request.user)
        context = {'friend_list': friend_list}
        return context

class FriendPage(LoginRequiredMixin, TemplateView):
    template_name = 'profile_view.html'
