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
            return redirect(group.id, RequestContext(request)) 
        return render(request, 'groups_create.html', {'form': form})    

class GroupListPage(ListView):
    model = Group
    template_name = 'group_search.html'

class GroupDetailPage(TemplateView):
    model = Group
    template_name = 'group_view.html'

    def get_context_data(self, username):
        creator_flag = False
        member_flag = False
        member_request_list = []
        member_request_flag = False
        requestee = User.objects.get(username = username)
        requested_group = Group.objects.get(pk = self.request.group)
        context = {'requestee': requestee}

        # Test if creator is self
        if requested_group.creator == requestee.username:
            creator_flag = True
            context['creator_flag'] = creator_flag
        
        # Test if user is member
        else:
            member_flag = Group.objects.is_member(self.request.user, requestee) == True
            context['member_flag'] = member_flag

        # Test if user add request is pending
        if member_request_flag == False:
            sent_group_requests = Group.objects.sent_requests(user=requestee)
            for user in sent_group_requests:
                member_request_list.append(user.to_user_id)
            friend_request_flag = requestee.profile.user_id in member_request_list
            context['member_request_flag'] = member_request_flag
        
        print(context)
        return context

class GroupSearchPage(TemplateView):
    template_name = 'group_search.html'

def create_group_add_request(request):
    pass