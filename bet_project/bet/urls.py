from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('play_bet/', views.play_bet, name='play_bet'),
    path('logout/', views.logout, name='logout'), 
    path('bet/success/', views.bet_success, name='bet_success'),
    path('bet/failure/', views.bet_failure, name='bet_failure'),
    path('profile/', views.profile, name='profile'),
]