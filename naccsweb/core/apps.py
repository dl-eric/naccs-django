from django.apps import AppConfig

import os
import requests

apikey = os.environ.get('FACEIT_KEY')

class CoreConfig(AppConfig):
    name = 'core'
    def ready(self):
        from .models import hubStats
        header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(apikey)
        }
        offset = 0
        total = 0
        res = requests.get("https://open.faceit.com/data/v4/hubs/a67c2ead-9968-4e8b-957b-fb8bc244b302/matches?type=past&offset=500&limit=1", headers=header)
        hubinfo = res.json()
        items = hubinfo['items']
        
        while len(items) != 0:
            res = requests.get("https://open.faceit.com/data/v4/hubs/a67c2ead-9968-4e8b-957b-fb8bc244b302/matches?type=past&offset="+ str(offset) +"&limit=100", headers=header) 
            hubinfo = res.json()
            items = hubinfo['items'] 
            total += len(items)
            offset += 100
        num = hubStats.objects.get(id=1)
        num.matches = int(total)
        num.save()
        
