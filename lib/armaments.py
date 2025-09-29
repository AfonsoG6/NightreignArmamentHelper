from os import path
from lib.constants import *
from threading import Lock
import json

GRABBABLE_SPECS: list[dict] = []
GRABBABLE_SPECS_LOCK: Lock = Lock()


def load_all_grabbable_specs(resources_path: str, language: str = DEFAULT_LANGUAGE) -> None:
    global GRABBABLE_SPECS, GRABBABLE_SPECS_LOCK
    with GRABBABLE_SPECS_LOCK:
        GRABBABLE_SPECS.clear()
        with open(path.join(resources_path, "armaments.json"), "r", encoding="utf-8") as file:
            armament_data = json.load(file)
            for armament in armament_data:
                GRABBABLE_SPECS.append(
                    {
                        "id": armament["id"],
                        "name": armament["name"][language],
                        "type": "armament",
                        "armament_type": armament["type"],
                        "STR": armament["STR"],
                        "DEX": armament["DEX"],
                        "INT": armament["INT"],
                        "FAI": armament["FAI"],
                        "ARC": armament["ARC"],
                    }
                )
        with open(path.join(resources_path, "items.json"), "r", encoding="utf-8") as file:
            item_data = json.load(file)
            for item in item_data:
                GRABBABLE_SPECS.append(
                    {
                        "id": f"i{item['id']}",
                        "name": item["name"][language],
                        "type": "item",
                    }
                )
        with open(path.join(resources_path, "talismans.json"), "r", encoding="utf-8") as file:
            talisman_data = json.load(file)
            for talisman in talisman_data:
                GRABBABLE_SPECS.append(
                    {
                        "id": f"t{talisman['id']}",
                        "name": talisman["name"][language],
                        "type": "talisman",
                    }
                )


def find_grabbable_name_by_id(grabbable_id: str) -> str:
    with GRABBABLE_SPECS_LOCK:
        for grabbable in GRABBABLE_SPECS:
            if grabbable["id"] == grabbable_id:
                return grabbable["name"]
    return ""

def get_all_grabbable_specs() -> list[dict]:
    with GRABBABLE_SPECS_LOCK:
        return GRABBABLE_SPECS.copy()
