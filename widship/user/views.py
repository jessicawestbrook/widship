from .forms import ProfileForm, NameSearchForm #, DeleteUserForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import ModelForm
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User
from logging import Logger
from ipware import get_client_ip
from .models import Profile, User
from geopy.geocoders import Nominatim
import requests
from django.contrib.gis.geos import Point, fromstr
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse



@login_required
def delete_user_view(request):
    pass
    try:
        u = User.objects.get(username = request.user.username)
        u.delete()          

    except User.DoesNotExist:
        messages.error(request, "User does not exist")    
        return render(request, 'signup.html')

    except Exception as e: 
        return render(request, 'settings.html')

    return render(request, 'login.html', {messages: messages.success(request, "Your account has been deleted")}) 

class NameSearchPage(ListView):
    model = Profile
    template_name = 'search_name.html'
    form = 'NameSearchForm'

def update_profile(request):
    profile = get_object_or_404(Profile, pk=request.user.id)
    submitted = False
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated.')
            return HttpResponseRedirect('profile')
        else:
            form = ProfileForm()
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'profile_form', {'form': form, 'submitted': submitted})

class ProfileFormPage(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'profile_form.html'

class ProfilePage(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'profile_view.html'

class ProfileDetailPage(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'profile_view.html'

class SearchPage(LoginRequiredMixin, TemplateView):
    template_name = 'search_results.html'
    model = Profile
    gps_coords = False
    location_result = False

    def get_user_ip(self):
        logger = Logger('logger')
        try:
            # Get IP
            client_ip, is_routable = get_client_ip(self.request)
            if client_ip is None:
                # Unable to get the client's IP address
                logger.info(msg="No client_ip")
            else:
                # We got the client's IP address
                if is_routable:
                    # The client's IP address is publicly routable on the Internet
                    logger.info(msg="client_ip: " + client_ip)
                    self.client_ip = client_ip
                else:
                    # The client's IP address is private
                    logger.info(msg="client_ip is private")
                    self.client_ip = client_ip
            return self
        except:
            logger.warn(msg="Error getting user IP")
            return self

    def get_user_location_from_address(self):
        logger = Logger('logger')
        #profile = get_object_or_404(Profile, pk=self.user.id)
        geolocator = Nominatim(user_agent="widship")
        self.location_result = geolocator.geocode("175 5th Avenue NYC")
        print(str(self.location_result.address))
        logger.info(msg='location: ' + str(self.location_result))
        self.gps_coords = fromstr(f'Point({self.location_result.longitude} {self.location_result.latitude})', srid=4326)
        return self

    def get_user_location_from_ip(self):
        logger = Logger('logger')
        if self.client_ip:
            try:
                # Get location from IP
                url = f"https://ipapi.co/{self.client_ip}/json/"
                logger.info(msg="search url: " + url)
                response = requests.get(url)
                response.raise_for_status()
                self.location_result = response.json()
                logger.info(msg="location_result: " + self.location_result)
            except:
                logger.warn(msg="Error getting user location") 
                self.get_user_location_from_address()
                return self
        else:
            try:
                self.get_user_location_from_address()
            except:
                logger.warn(msg="No address listed")
                return self

    def save_location_to_db(self):
        # Save user location to database
        user_profile = self.request.user
        user_profile.gps_coords=fromstr(f'Point({self.location_result.longitude} {self.location_result.latitude})', srid=4326)
        user_profile.profile.save()
        return self

    def user_search(self):
        self.search_results = Profile.objects.all().annotate(distance=Distance('gps_coords', self.gps_coords)).order_by('distance')

    def get_context_data(self):
        logger = Logger('logger')
        context = super().get_context_data()
        # Return query results
        self.client_ip = '68.60.92.109'
        self.get_user_location_from_ip()
        self.save_location_to_db()
        self.user_search()
        context['search_results'] = self.search_results
        return context