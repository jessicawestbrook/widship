from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
import requests

# Create your views here.

class GroupsPage(TemplateView):
    template_name = 'groups.html'

class GroupPage(TemplateView):
    template_name = 'group.html'

class GroupSearchPage(TemplateView):
    template_name = 'group_search.html'

class GroupCreatePage(TemplateView):
    template_name = 'groups_create.html'

def create_group_add_request(request):
    pass