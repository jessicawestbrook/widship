from django.apps import AppConfig

class WidshipConfig(AppConfig):
    name = 'widship'

    def ready(self):
        from actstream import registry
        from django.contrib.auth.models import User
        registry.register(User)