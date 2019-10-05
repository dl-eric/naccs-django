from django.apps import AppConfig
from watson import search as watson

class LeagueConfig(AppConfig):
    name = 'league'
    def ready(self):
        Schools = self.get_model("School")
        watson.register(Schools, fields=["name"])
