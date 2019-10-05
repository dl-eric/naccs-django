import os
import requests
from .models import HubStats

apikey = os.environ.get('FACEIT_KEY')
def get_matches():
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
    num = HubStats.objects.get(id=1)
    num.matches = int(total)
    num.save()

url = 'https://open.faceit.com/data/v4/hubs/a67c2ead-9968-4e8b-957b-fb8bc244b302'

players = {}
def get_hub_stats():
    header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(apikey)
    }
    try:
        res = requests.get(url+'?expanded=organizer', headers=header)
        hubinfo = res.json()
        players = hubinfo['players_joined']
        return players
    except:
        print('error')
        players = 0
        return players