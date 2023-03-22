import openai

from .. import models


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
                    "You are the only player of a fantasy RPG tabletop game, which is "
                    "being run by a Game Master. Your character is called "
                    f"{character.name} and they are a {character.race_name} "
                    f"{character.class_name}."
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
            "content": f"{last_turn.description} Describe how you react to this. Only "
            "write a short paragraph.",
        }
    ]
