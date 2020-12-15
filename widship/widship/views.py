from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.models import User




class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

class AttributionsPage(TemplateView):
    template_name = 'attributions.html'

class CookiesPage(TemplateView):
    template_name = 'cookies.html'

class PrivacyPage(TemplateView):
    template_name = 'privacy.html'

class TermsPage(TemplateView):
    template_name = 'terms.html'

class SettingsPage(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'
