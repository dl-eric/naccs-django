from django.shortcuts import render
from .models import hubStats
import os
import requests

# Create your views here.
apikey = os.environ.get('FACEIT_KEY')
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
    

def index(request):
    player = get_hub_stats()
    num_matches = hubStats.objects.get(id=1)
    return render(request, 'core/index.html', {'main': True, 'player_count': player, 'num_matches': num_matches.matches})