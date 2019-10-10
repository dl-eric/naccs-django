import os
import requests

URL = 'https://open.faceit.com/data/v4/leaderboards/hubs/'
HUB_ID = 'a67c2ead-9968-4e8b-957b-fb8bc244b302'
FACEIT_KEY = os.environ.get('FACEIT_KEY')


def get_hub_leaderboard():
    header = {
        'accept': 'application/json',
        'Authorization': 'Bearer {}'.format(FACEIT_KEY)
    }
    try:
        res = requests.get(
            URL + HUB_ID + '/seasons/1?offset=0&limit=10', headers=header)
        leaderboard = res.json()
        players = leaderboard['items']
        print(players)
        return players
    except:
        print('error')
        players = 0
        return players
