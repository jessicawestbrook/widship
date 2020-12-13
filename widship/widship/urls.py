"""widship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include, url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static



urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/icons/eternity_16_16.png', permanent=True)),
    url('', include('pwa.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('messaging/', include('postman.urls', namespace='messaging')),
    path('activity/', include('actstream.urls')),
    path('friendship/', include('friendship.urls')),
    path('friends/', include('friends.urls', namespace='friends')),
    path('user/', include('user.urls')),
    path('', views.HomePage.as_view(), name='home'),
    path('settings', views.SettingsPage.as_view(), name='settings'),
    path('attributions', views.AttributionsPage.as_view(), name='attributions'),
    path('cookies', views.CookiesPage.as_view(), name='cookies'),
    path('terms', views.TermsPage.as_view(), name='terms'),
    path('privacy', views.PrivacyPage.as_view(), name='privacy'),
    path('login', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    url(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

