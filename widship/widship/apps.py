from django.apps import AppConfig
from django.db.models.signals import post_migrate

class WidshipConfig(AppConfig):
    name = 'widship'

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import User
        registry.register(User)