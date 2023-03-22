import re
from dataclasses import dataclass

import openai


@dataclass
class CharacterDescription:
    full_description: str
    name: str
    race: str
    class_: str
    visual_description: str
    personality: str
    backstory: str


def get_openai_character_description(
    character_prompt: str = "",
) -> CharacterDescription:
    full_description = _get_full_character_description(character_prompt)
    return _get_character_description(full_description)


def _get_full_character_description(character_prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a character creator for a game of D&D 5th Edition.",
            },
            {
                "role": "user",
                "content": "Describe a D&D character, including the name, race, class, visual "
                f"description, personality, and backstory. {character_prompt}",
            },
        ],
    )
    return response.choices[0]["message"]["content"]


def _get_character_description(full_description: str) -> CharacterDescription:
    """
    Try to use regex to pull out the attributes from the prompt.
    """

    full_description = full_description.replace("\n", " ")

    name = _get_attribute(r".*Name:(.*?)Race:.*", full_description)
    race = _get_attribute(r".*Race:(.*?)Class:.*", full_description)
    class_ = _get_attribute(r".*Class:(.*?)Visual Description:.*", full_description)
    visual_description = _get_attribute(
        r".*Visual Description:(.*?)Personality:.*", full_description
    )
    personality = _get_attribute(r".*Personality:(.*?)Backstory:.*", full_description)
    backstory = _get_attribute(r".*Backstory:(.*)", full_description)

    return CharacterDescription(
        full_description, name, race, class_, visual_description, personality, backstory
    )


def _get_attribute(regex_pattern: str, full_description: str) -> str:
    """
    Try to pull out a single attribute from the full description, by returning the
    first match for the given regex pattern.
    """

    match = re.match(regex_pattern, full_description)

    # It might be more accurate to throw an exception here
    if not match:
        return ""

    return match[1].strip()
