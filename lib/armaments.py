from os import path
import json

GRABBABLE_SPECS: list[dict] = []

def load_all_grabbable_specs(resources_path: str) -> None:
    global GRABBABLE_SPECS
    with open(path.join(resources_path, "armaments.json"), "r", encoding="utf-8") as file:
        armament_data = json.load(file)
        for armament in armament_data:
            GRABBABLE_SPECS.append(
                {
                    "id": armament["id"],
                    "name": armament["name"],
                    "type": "armament",
                    "armament_type": armament["type"],
                    "STR": armament["STR"],
                    "DEX": armament["DEX"],
                    "INT": armament["INT"],
                    "FAI": armament["FAI"],
                    "ARC": armament["ARC"]
                }
            )
    with open(path.join(resources_path, "items.json"), "r", encoding="utf-8") as file:
        item_data = json.load(file)
        for item in item_data:
            GRABBABLE_SPECS.append(
                {
                    "id": f"i{item['id']}",
                    "name": item["name"],
                    "type": "item",
                }
            )
    with open(path.join(resources_path, "talismans.json"), "r", encoding="utf-8") as file:
        talisman_data = json.load(file)
        for talisman in talisman_data:
            GRABBABLE_SPECS.append(
                {
                    "id": f"t{talisman['id']}",
                    "name": talisman["name"],
                    "type": "talisman",
                }
            )


def find_grabbable_name_by_id(grabbable_id: str) -> str:
    for grabbable in GRABBABLE_SPECS:
        if grabbable["id"] == grabbable_id:
            return grabbable["name"]
    return ""
