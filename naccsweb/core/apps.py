from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from .faceit import get_matches
        from .models import HubStats
        get_matches()
        
        
