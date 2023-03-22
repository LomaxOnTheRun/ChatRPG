from django.urls import path

from . import views


urlpatterns = [
    path(
        "character-creation/",
        views.CharacterCreation.as_view(),
        name="character_creation",
    ),
]
