import openai

from .. import models


def get_one_player_game_intro(character: models.Character) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Game Master running a fantasy RPG tabletop game for a "
                    f"single player. Their character is called {character.name} and "
                    f"they are a {character.race_name} {character.class_name}."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Describe the start of a new adventure. Do not describe anything "
                    "that will happen in the future. Only write a short paragraph."
                ),
            },
        ],
    )
    return response.choices[0]["message"]["content"]


def get_one_player_game_next_description(
    character: models.Character, game: models.OnePlayerGame
) -> str:
    previous_messages = _get_previous_messages(game)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Game Master running a fantasy RPG tabletop game for a "
                    f"single player. Their character is called {character.name} and "
                    f"they are a {character.race_name} {character.class_name}."
                ),
            },
            *previous_messages,
        ],
    )
    return response.choices[0]["message"]["content"]


def _get_previous_messages(game: models.OnePlayerGame) -> list[dict[str, str]]:
    game_turns = models.OnePlayerGameTurn.objects.filter(game=game).order_by(
        "created_at"
    )

    last_turn = game_turns.last()

    # TODO: Return more previous turns
    return [
        {
            "role": "user",
            "content": f"{last_turn.description} Describe what happens next in the "
            "story. Only write a short paragraph.",
        }
    ]
