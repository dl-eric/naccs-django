from django.apps import AppConfig
from watson import search as watson

class LeagueConfig(AppConfig):
    name = 'league'
    def ready(self):
        Schools = self.get_model("School")
        Players = self.get_model('Player')
        watson.register(Schools, fields=["name"])
        watson.register(Players, fields=["user"])
