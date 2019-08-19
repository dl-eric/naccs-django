from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import base64
from django.contrib.auth.decorators import login_required
import requests
import os

DISCORD_ENDPOINT = 'https://discordapp.com/api'
DISCORD_TOKEN_URL = DISCORD_ENDPOINT + '/oauth2/token'
DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')

FACEIT_TOKEN_ENDPOINT = 'https://api.faceit.com/auth/v1/oauth/token'
FACEIT_INFO_ENDPOINT = 'https://api.faceit.com/auth/v1/resources/userinfo'
FACEIT_CLIENT_ID = os.environ.get('FACEIT_CLIENT_ID')
FACEIT_CLIENT_SECRET = os.environ.get('FACEIT_CLIENT_SECRET')

def get_discord_name(code):
    data = {
        'client_id':        DISCORD_CLIENT_ID,
        'client_secret':    DISCORD_CLIENT_SECRET,
        'grant_type':       'authorization_code',
        'code':             code,
        'redirect_uri':     'http://localhost:8000/settings/account/discordcallback',
        'scope':            'identify'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers).json()
    access_token = r.get('access_token')

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    r = requests.get(DISCORD_ENDPOINT + '/users/@me', headers=headers)
    return r.json()['username']

def get_faceit_name(faceit_code):
    data = {
        'code': faceit_code,
        'grant_type': 'authorization_code'
    }

    authorization = f'{FACEIT_CLIENT_ID}:{FACEIT_CLIENT_SECRET}'.encode()
    authorization_enc = base64.b64encode(authorization)
    headers = {
        'Authorization': 'Basic ' + authorization_enc.decode()
    }

    # exchange code for authorization token
    response = requests.post(FACEIT_TOKEN_ENDPOINT, data=data, headers=headers)

    access_token = response.json().get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response =  requests.get(FACEIT_INFO_ENDPOINT, headers=headers)
    return response.json().get('nickname')

@login_required
def account(request):
    return render(request, 'settings/account.html')

@login_required
def faceit(request):
    faceit_code = request.GET.get('code')
    faceit_username = get_faceit_name(faceit_code)

    # Enter faceit name into user profile
    user = User.objects.get(username=request.user.username)
    user.profile.faceit = faceit_username
    user.save()

    return redirect('account')
    
@login_required
def discord(request):
    discord_code = request.GET.get('code')
    discord_name = get_discord_name(discord_code)

    # Enter discord name into user profile
    user = User.objects.get(username=request.user.username)
    user.profile.discord = discord_name
    user.save()
    return redirect('account')