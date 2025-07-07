from os import path
import json

# Changed DEX from B to A for DUCHESS due to the real stats actually being 1 point apart.
CHARACTER_SPECS: list[dict] = []

def load_all_character_specs(resources_path: str) -> None:
    global CHARACTER_SPECS
    with open(path.join(resources_path, "characters.json"), "r", encoding="utf-8") as file:
        character_data = json.load(file)
        for character in character_data:
            CHARACTER_SPECS.append(
                {
                    "name": character["name"],
                    "weapon_types": character["weapon_types"],
                    "STR": character["STR"],
                    "DEX": character["DEX"],
                    "INT": character["INT"],
                    "FAI": character["FAI"],
                    "ARC": character["ARC"]
                }
            )