from django.apps import AppConfig
from django.conf import settings as django_settings


class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from .faceit import get_matches_total
        from .models import HubStats

        if not django_settings.DEBUG:
            try:
                total = get_matches_total()
                num = HubStats.objects.get(id=1)
                num.matches = int(total)
                num.save()
            except:
                # Do nothing
                return
        
        
