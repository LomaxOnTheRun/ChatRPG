from django import http
from django import forms as django_forms
from django.views import generic

from . import forms, models
from .domain import gm_descriptions


class Home(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)

        context["characters"] = models.Character.objects.all()

        return context


class CharacterCreation(generic.FormView):
    template_name = "character-creation.html"
    form_class = forms.CharacterCreationForm
    success_url = "/"

    def form_valid(self, form: forms.CharacterCreationForm) -> http.HttpResponse:
        if form.is_valid():
            models.Character.objects.create(
                name=form.cleaned_data["name"],
                race_name=form.cleaned_data["race_name"],
                class_name=form.cleaned_data["class_name"],
                visual_description=form.cleaned_data["visual_description"],
                personality=form.cleaned_data["personality"],
                backstory=form.cleaned_data["backstory"],
            )

        return super().form_valid(form)


class OnePlayerGameStart(generic.FormView):
    template_name = "one-player-game-start.html"
    form_class = django_forms.Form  # We just need a "submit button"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)

        character = models.Character.objects.get(id=self.kwargs["character_id"])
        context["character"] = character

        context["intro_description"] = gm_descriptions.get_one_player_game_intro(
            character
        )

        return context

    def form_valid(self, form: django_forms.Form) -> http.HttpResponse:
        context = self.get_context_data()
        character = context["character"]

        # Create a new game, and the initial turn for that game
        one_player_game = models.OnePlayerGame.objects.create(character=character)
        models.OnePlayerGameTurn.objects.create(
            game=one_player_game,
            character=None,  # The GM
            description=context["intro_description"],
        )

        return http.HttpResponseRedirect(
            f"/one-player-game/{character.id}/{one_player_game.id}"
        )
