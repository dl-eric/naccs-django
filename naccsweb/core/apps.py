from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from .faceit import get_matches_total
        from .models import HubStats
        total = get_matches_total()
        num = HubStats.objects.get(id=1)
        num.matches = int(total)
        num.save()
        
        
