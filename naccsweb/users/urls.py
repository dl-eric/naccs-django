from django.urls import path

from . import views
from .decorators import logout_required

urlpatterns = [
    path(r'users', views.profile_search, name='search'),
    path(r'users/<page_alias>', views.profile, name='profile'),
    path(r'register/', logout_required(views.register), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', logout_required(views.activate), name='activate'),
    path(r'register/pending', logout_required(views.pending), name='pending_confirmation'),
    path(r'register/confirmed', logout_required(views.confirmed), name='confirmed'),
    path(r'notfound/', views.not_found, name='not_found')
]