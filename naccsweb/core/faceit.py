import os
import requests
from .models import HubStats

URL = 'https://open.faceit.com/data/v4/hubs/'
HUB_ID = 'a67c2ead-9968-4e8b-957b-fb8bc244b302'
FACEIT_KEY = os.environ.get('FACEIT_KEY')

def get_matches_total():
    header = {
            'accept': 'application/json',
            'Authorization': 'Bearer {}'.format(FACEIT_KEY)
            }
    offset = 0
    total = 0
    res = requests.get(URL+ HUB_ID +"/matches?type=past&offset=500&limit=1", headers=header)
    hubinfo = res.json()
    items = hubinfo['items']
            
    while len(items) != 0:
        res = requests.get(URL+ HUB_ID +"/matches?type=past&offset="+ str(offset) +"&limit=100", headers=header) 
        hubinfo = res.json()
        items = hubinfo['items'] 
        total += len(items)
        offset += 100
    return total



players = {}
def get_hub_size():
    header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(FACEIT_KEY)
    }
    try:
        res = requests.get(URL+ HUB_ID +'?expanded=organizer', headers=header)
        hubinfo = res.json()
        players = hubinfo['players_joined']
        return players
    except:
        print('error')
        players = 0
        return players