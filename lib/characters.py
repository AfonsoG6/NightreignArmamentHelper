from os import path
from lib.constants import *
import json

# Changed DEX from B to A for DUCHESS due to the real stats actually being 1 point apart.
CHARACTER_SPECS: list[dict] = []

def load_all_character_specs(resources_path: str, language: str = DEFAULT_LANGUAGE) -> None:
    global CHARACTER_SPECS
    CHARACTER_SPECS.clear()
    with open(path.join(resources_path, "characters.json"), "r", encoding="utf-8") as file:
        character_data = json.load(file)
        for character in character_data:
            CHARACTER_SPECS.append(
                {
                    "id": character["id"],
                    "name": character["name"][language],
                    "armament_types": character["armament_types"],
                    "STR": character["STR"],
                    "DEX": character["DEX"],
                    "INT": character["INT"],
                    "FAI": character["FAI"],
                    "ARC": character["ARC"]
                }
            )


def find_character_by_name(character_name: str) -> dict | None:
    for character in CHARACTER_SPECS:
        if character["name"] == character_name:
            return character
    return None

def find_character_by_id(character_id: int) -> dict | None:
    for character in CHARACTER_SPECS:
        if character["id"] == character_id:
            return character
    return None