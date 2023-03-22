from django.urls import path

from . import views


urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path(
        "character-creation",
        views.CharacterCreation.as_view(),
        name="character_creation",
    ),
    path(
        "one-player-game/<int:character_id>",
        views.OnePlayerGameStart.as_view(),
        name="one_player_game_start",
    ),
]
