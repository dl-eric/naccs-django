from django.urls import path

from . import views

urlpatterns = [
    path(r'account', views.account, name='account'),
    path(r'account/faceitconfirm', views.faceit, name='faceitconfirm'),
    path(r'account/discordcallback', views.discord, name='discord')
]