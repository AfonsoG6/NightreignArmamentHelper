from os import path
from lib.constants import *
from threading import Lock
import json

# Changed DEX from B to A for DUCHESS due to the real stats actually being 1 point apart.
CHARACTER_SPECS: list[dict] = []
CHARACTER_SPECS_LOCK: Lock = Lock()

def load_all_character_specs(resources_path: str, language: str = DEFAULT_LANGUAGE) -> None:
    global CHARACTER_SPECS
    with CHARACTER_SPECS_LOCK:
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
    with CHARACTER_SPECS_LOCK:
        for character in CHARACTER_SPECS:
            if character["name"] == character_name:
                return character
    return None

def find_character_by_id(character_id: int) -> dict | None:
    with CHARACTER_SPECS_LOCK:
        for character in CHARACTER_SPECS:
            if character["id"] == character_id:
                return character
    return None


def get_all_character_specs() -> list[dict]:
    with CHARACTER_SPECS_LOCK:
        return CHARACTER_SPECS.copy()

def get_all_character_names() -> list[str]:
    with CHARACTER_SPECS_LOCK:
        return [character["name"] for character in CHARACTER_SPECS]