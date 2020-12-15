from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .forms import GroupForm
from django.shortcuts import render, get_object_or_404
from .models import Group
from django.views.generic.base import RedirectView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import User
#from django.shortcuts import render_to_response

# Create your views here.

class GroupFormPage(LoginRequiredMixin, TemplateView):
    model = Group
    template_name = 'groups_create.html'
    context_object_name = 'group'


@login_required
def create_group(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST': 
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid(): 
            group = form.save(commit=False)
            group.creator_username = request.user.username
            group.save() 
            messages.success(request, "You've created the group " + group.name)
            return redirect('group.id', RequestContext(request)) 
        return render(request, 'groups_create.html', {'form': form})    

class GroupsPage(TemplateView):
    template_name = 'groups.html'

class GroupPage(TemplateView):
    template_name = 'group.html'

class GroupSearchPage(TemplateView):
    template_name = 'group_search.html'

def create_group_add_request(request):
    pass