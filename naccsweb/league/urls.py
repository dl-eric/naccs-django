from django.urls import path

from . import views

urlpatterns = [
    path(r'school/', views.school_search, name='school_search'),
    path(r'school/<school_id>', views.school, name='school'),
    path(r'hub', views.hub, name='hub'),
    path(r'league', views.league, name='league')
]