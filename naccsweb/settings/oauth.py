import requests
import os   
import base64
import json
import logging

DISCORD_ENDPOINT = 'https://discordapp.com/api'
DISCORD_TOKEN_URL = DISCORD_ENDPOINT + '/oauth2/token'
DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')

FACEIT_TOKEN_ENDPOINT = 'https://api.faceit.com/auth/v1/oauth/token'
FACEIT_INFO_ENDPOINT = 'https://api.faceit.com/auth/v1/resources/userinfo'
FACEIT_INVITE_ENDPOINT = 'https://api.faceit.com/invitations/v1/invite'
FACEIT_CLIENT_ID = os.environ.get('FACEIT_CLIENT_ID')
FACEIT_CLIENT_SECRET = os.environ.get('FACEIT_CLIENT_SECRET')
FACEIT_HUB_BOT_TOKEN = os.environ.get('FACEIT_HUB_BOT_TOKEN')

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
    return r.json()['username'] + '#' + r.json()['discriminator']

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

def get_collegiate_invite():
    data = {
        "entity_id":"a67c2ead-9968-4e8b-957b-fb8bc244b302",
	    "entity_type":"hub",
	    "type":"regular",
	    "max_age":0,
	    "max_uses":1
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + FACEIT_HUB_BOT_TOKEN
    }

    response = requests.post(FACEIT_INVITE_ENDPOINT, data=json.dumps(data), headers=headers).json()
    print("Response", response)
    if response.get('code') and response.get('code') == 'OPERATION-OK':
        code = response.get('payload').get('code')
        return code
    
    logging.error("Failed to get invite", exc_info=True)
    return None

def get_invite_link(code):
    return 'https://www.faceit.com/en/inv/' + code