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
