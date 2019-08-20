from django.urls import path

from . import views

urlpatterns = [
    path('verify/<slug:uidb64>/<slug:token>)/', views.verify, name='verify'),
    path(r'account/pending', views.pending, name='pending'),
    path(r'account', views.account, name='account'),
    path(r'account/faceitconfirm', views.faceit, name='faceitconfirm'),
    path(r'account/discordcallback', views.discord, name='discord')
]