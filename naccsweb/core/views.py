from django.shortcuts import render
from .models import HubStats
import os
import requests
from .faceit import get_hub_size

# Create your views here.

def index(request):
    player = get_hub_size()
    num_matches = HubStats.objects.get(id=1)
    return render(request, 'core/index.html', {'main': True, 'player_count': player, 'num_matches': num_matches.matches})