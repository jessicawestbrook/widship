from django import template
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from friendship.models import Friend, Follow, Block, FriendshipRequest
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create_friend_request(request, username):
    other_user = User.objects.get(username = username)
    Friend.objects.add_friend(
        request.user,                               # The sender
        other_user,                                 # The recipient
        message='Hi! I would like to add you')      # This message is optional
    messages.success(request, "You've sent a friend request to " + other_user.profile.profile_name)
    return render(request, 'search_results')

class FriendRequestsPage(LoginRequiredMixin, ListView):
    Profile = apps.get_model('user', 'Profile')
    model = Friend
    context_object_name = 'friend_request_list'
    template_name = 'friend_list.html'

    def __init__(self):
        super(FriendsPage, self).__init__()

    def get_context_data(self):
        Profile = apps.get_model('user', 'Profile')
        friend_list = Friend.objects.friends(self.request.user)
        #friend_list = Friend.objects.filter(from_user = self.request.user)
        context = {'friend_list': friend_list}
        return context
        friend_request = FriendshipRequest.objects.get(to_user=request.to_user)

def accept_friend_request(request):
    friend_request = FriendshipRequest.objects.get(to_user=request.to_user)
    friend_request.accept()
    messages.success(request, "You're friends with " + friend_request.from_user.profile.profile_name)

def reject_friend_request(request):
    friend_request = FriendshipRequest.objects.get(to_user=request.to_user)
    friend_request.reject()

def unfriend(request):
    other_user = User.objects.get(username = request.other_user.username)
    Friend.objects.remove_friend(request.user, other_user)
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
