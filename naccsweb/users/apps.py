from django.apps import AppConfig
from watson import search as watson

class UsersConfig(AppConfig):
    name = 'users'
    def ready(self):
        Users = self.get_model("Profile")
        watson.register(Users, fields=["nickname"])
