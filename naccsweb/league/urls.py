from django.urls import path

from . import views

urlpatterns = [
    path(r'school/', views.school_search, name='school_search'),
    path(r'school/<school_id>', views.school, name='school'),
    path(r'hub', views.hub, name='hub'),
    path(r'league', views.league, name='league'),
    path(r'create_team/<school_id>', views.create_team, name='create_team'),
    path(r'team_pending', views.team_pending, name='team_pending'),
    path(r'join_team/<school_id>', views.join_team, name='join_team'),
    path(r'manage_team/<team_id>', views.manage_team),
    path(r'one_payment', views.one_payment, name='one_payment'),
    path(r'two_payment', views.two_payment, name='two_payment'),
    path(r'one_sub_payment', views.one_sub_payment, name='one_sub_payment'),
    path(r'two_sub_payment', views.two_sub_payment, name='two_sub_payment'),
    path(r'payment_return', views.payment_return, name='payment_return'),
    path(r'payment_return?success=true',
         views.payment_return, name='payment_return_success'),
    path(r'payment_return?cancel=true',
         views.payment_return, name='payment_return_cancel'),
    path(r'kick_user', views.kick_user)
]
