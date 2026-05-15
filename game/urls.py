from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game_lobby, name='game_lobby'),
    path('game/<int:test_id>/classic/', views.game_play, {'mode': 'classic'}, name='game_classic'),
    path('game/<int:test_id>/speed/', views.game_play, {'mode': 'speed'}, name='game_speed'),
    path('game/<int:test_id>/survival/', views.game_play, {'mode': 'survival'}, name='game_survival'),
]
