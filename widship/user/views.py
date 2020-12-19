from urllib.request import urlopen
from .forms import ProfileForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.forms import ModelForm
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth.models import User
from logging import Logger
from ipware import get_client_ip
from .models import Profile, User
from geopy.geocoders import Nominatim
from django.template import RequestContext
from PIL import Image
#from urllib.request import urlopen
import urllib3
import requests
from io import BytesIO
from django.core.files.base import ContentFile, File
from django.contrib.gis.geos import Point, fromstr
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from friendship.models import Friend
from django.dispatch import receiver
from allauth.account.signals import user_signed_up



@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):    
    if sociallogin.account.provider == 'facebook':
        try:
            user.profile = get_object_or_404(Profile, user=user)
        except:
            user.profile = Profile.objects.create(user=user)
        user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
        #picture_url = user_data['url']
        #picture_url = user_data['url']
        #user.profile.fb_link = picture_url
        print('user_data: ', user_data)
        print('user_data.email: ', user_data['email'])
        #print('user_data.url: ', user_data['url'])
        print('user: ', user)
        print('user.profile: ', user.profile)
        try:
            #picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
            #picture_url = "http://graph.facebook.com/" + user_data['id'] + "/picture?type=large"
            #picture_url = "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=10113901811345443&height=50&width=50&ext=1610820110&hash=AeTs4e0GeiYcI0RN8Ac"
            #response = requests.get(picture_url)
            #picture_url = "http://graph.facebook.com/%s/picture?type=large" % user_data["id"]

            picture_data = user_data['picture']
            picture_data = picture_data['data']
            picture_url = picture_data['url']
            print("picture_url: ", picture_url)
            photo = urlopen(picture_url)
            print('photo: ', photo)
            #print('response: ', response.__dict__)
            #canvas = Image.new('RGB', (200, 200), 'white')
            #profile_photo = Image.open(BytesIO(response.content))
            #profile_photo_blob = BytesIO(response.content)
            #canvas.save(profile_photo_blob, 'JPEG')  
            #print('profile_photo_blob: ', profile_photo_blob)
            #user.profile.profile_photo = profile_photo
            #user.profile.profile_photo.save(user.username + '.jpg', photo, save=False)
            user.profile.profile_photo.save(user.username + '.jpg', ContentFile(photo.read()), save=False)
            #user.profile.profile_photo = profile_photo or None
        except:
            print("Couldn't get Facebook profile photo.")  
        #print('picture_url: ', picture_url)         
        user.email = user_data['email'] or None
        user.first_name = user_data['first_name'] or None
        user.last_name = user_data['last_name'] or None
        user.profile.save()  
        return HttpResponse('profile_form.html')

@login_required
def delete_user_view(request):
    try:
        u = User.objects.get(username = request.user.username)
        u.delete()          

    except User.DoesNotExist:
        messages.error(request, "User does not exist")    
        return render(request, 'signup.html')

    except Exception as e: 
        return render(request, 'settings.html')

    return render(request, 'login.html', {messages: messages.success(request, "Your account has been deleted")}) 

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
    context_object_name = 'context'

class ProfileDetailPage(LoginRequiredMixin, TemplateView):
    model = Profile
    template_name = 'profile_view.html'

    def get_context_data(self, username):
        self_flag = False
        friend_flag = False
        friends_request_list = []
        friend_request_flag = False
        requested_profile_user = User.objects.get(username = username)
        context = {'requested_profile_user': requested_profile_user}

        # Test if user is self
        if self.request.user.username == requested_profile_user.username:
            self_flag = True
            context['self_flag'] = self_flag
        
        # Test if users are friends
        else:
            friend_flag = Friend.objects.are_friends(self.request.user, requested_profile_user) == True
            context['friend_flag'] = friend_flag

        # Test if friend request is pending
        if friend_flag == False:
            sent_friend_requests = Friend.objects.sent_requests(user=self.request.user)
            for user in sent_friend_requests:
                friends_request_list.append(user.to_user_id)
            friend_request_flag = requested_profile_user.profile.user_id in friends_request_list
            context['friend_request_flag'] = friend_request_flag
        
        print(context)
        return context
class SearchPage(LoginRequiredMixin, TemplateView):
    template_name = 'search_results.html'
    model = User
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
        exclude_user_id_list = [self.request.user.profile.user_id]
        user_friends = Friend.objects.friends(self.request.user)
        if user_friends:
            for friend in user_friends:
                exclude_user_id_list.append(friend.id)
        search_results = Profile.objects.exclude(user_id__in=exclude_user_id_list).annotate(distance=Distance('gps_coords', self.gps_coords)).order_by(self.search_parameters.get('sort'))
        self.search_results = search_results
        return self

    def get_context_data(self):
        context = super().get_context_data()

        # Get query parameters
        search_distance = self.request.GET.get('distance') or '50'
        search_distance_unit = self.request.GET.get('distance-unit') or 'miles'
        search_age = self.request.GET.get('age') or 100
        search_gender = self.request.GET.get('gender') or 'both'
        search_sort = self.request.GET.get('sort') or 'distance'
        search_name = self.request.GET.get('name') or ''
        self.search_parameters = {'distance': search_distance, 'distance_unit': search_distance_unit, 'age': search_age, 'gender': search_gender, 'sort': search_sort, 'name': search_name}
        print('search_parameters: ', self.search_parameters)
        context['search_parameters'] = self.search_parameters

        # Return query results
        self.client_ip = '68.60.92.109'
        self.get_user_location_from_ip()
        self.save_location_to_db()
        self.user_search()
        context['search_results'] = self.search_results
        return context