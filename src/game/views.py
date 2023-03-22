from django import http
from django import forms as django_forms
from django.views import generic

from . import forms, models
from .domain import gm_descriptions, player_descriptions


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

    # This is a super hacky way of accessing data generated by `get_context_data` in
    # `form_valid`
    extra_context = {}

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)

        character = models.Character.objects.get(id=self.kwargs["character_id"])
        context["character"] = character

        intro_description = gm_descriptions.get_one_player_game_intro(character)
        # intro_description = "Something, something, tavern..."
        context["intro_description"] = intro_description

        self.extra_context["character"] = character
        self.extra_context["intro_description"] = intro_description

        return context

    def form_valid(self, form: django_forms.Form) -> http.HttpResponse:
        character = self.extra_context["character"]
        intro_description = self.extra_context["intro_description"]

        # Create a new game, and the initial turn for that game
        game = models.OnePlayerGame.objects.create(character=character)
        models.OnePlayerGameTurn.objects.create(
            game=game,
            character=None,  # The GM
            description=intro_description,
        )

        # Also create the first player turn
        first_player_description = (
            player_descriptions.get_one_player_game_next_description(character, game)
        )
        models.OnePlayerGameTurn.objects.create(
            game=game,
            character=character,
            description=first_player_description,
        )

        return http.HttpResponseRedirect(f"/one-player-game/{character.id}/{game.id}")


class OnePlayerGame(generic.FormView):
    template_name = "one-player-game.html"
    form_class = django_forms.Form  # We just need a "submit button"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)

        character = models.Character.objects.get(id=self.kwargs["character_id"])
        context["character"] = character

        game_id = self.kwargs["one_player_game_id"]
        game_turns = models.OnePlayerGameTurn.objects.filter(game_id=game_id).order_by(
            "created_at"
        )
        context["game_turns"] = game_turns

        return context

    def form_valid(self, form: django_forms.Form) -> http.HttpResponse:
        context = self.get_context_data()
        character = context["character"]
        game_turns = context["game_turns"]

        last_game_turn = game_turns.last()
        game = last_game_turn.game

        if last_game_turn.character is None:
            # It's now the player's turn
            description = player_descriptions.get_one_player_game_next_description(
                character, game
            )
            models.OnePlayerGameTurn.objects.create(
                game=game,
                character=character,
                description=description,
            )
        else:
            # It's now the GM's turn
            # TODO: Create a new domain function for this
            pass

        # Reload the same page
        return http.HttpResponseRedirect("")
