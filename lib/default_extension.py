# ----------------------------------------------------------------------- Constants ----------------------------------------------------------------------------

TYPE_MATCH_ICON = "\U0001f9e4"
GREAT_MATCH_ICON = "\u2b50"
DECENT_MATCH_ICON = "\u2714"

# -------------------------------------------------------------------- Helper functions ------------------------------------------------------------------------


def get_stat_value(rating: str) -> int:
    ratings = {
        "S": 32,
        "A": 16,
        "B": 8,
        "C": 4,
        "D": 2,
        "E": 1,
    }
    return ratings.get(rating, 0)


def get_sum_two_best_stats(character_spec: dict) -> int:
    stats = [character_spec["STR"], character_spec["DEX"], character_spec["INT"], character_spec["FAI"], character_spec["ARC"]]
    stat_values = [get_stat_value(stat) for stat in stats]
    stat_values.sort(reverse=True)
    return stat_values[0] + stat_values[1]


def convert_stat_to_rating(stat_name: str, stat_value: int) -> str:
    if stat_value == 0:
        return "-"
    if stat_name in ["STR", "DEX"]:
        if stat_value < 15:
            return "E"
        elif stat_value < 30:
            return "D"
        elif stat_value < 45:
            return "C"
        elif stat_value < 60:
            return "B"
        elif stat_value < 75:
            return "A"
        else:
            return "S"
    elif stat_name in ["INT", "FAI"]:
        if stat_value < 20:
            return "E"
        elif stat_value < 30:
            return "D"
        elif stat_value < 40:
            return "C"
        elif stat_value < 50:
            return "B"
        elif stat_value < 60:
            return "A"
        else:
            return "S"
    elif stat_name == "ARC":
        if stat_value < 10:
            return "E"
        elif stat_value < 20:
            return "D"
        elif stat_value < 40:
            return "C"
        elif stat_value < 60:
            return "B"
        elif stat_value < 80:
            return "A"
        else:
            return "S"
    return "-"


# --------------------------------------------------------------------- Main functions -------------------------------------------------------------------------


def get_basic_label_icons(character_spec: dict, grabbable_spec: dict) -> list[str]:
    icons: list[str] = []
    if grabbable_spec["type"] != "armament":
        return []

    score: int = 0
    stats: list[str] = ["STR", "DEX", "INT", "FAI", "ARC"]
    for stat in stats:
        armament_stat: int = get_stat_value(convert_stat_to_rating(stat, grabbable_spec.get(stat, 0)))
        character_stat: int = get_stat_value(character_spec[stat])
        score += armament_stat * character_stat
    average_score: float = score / (get_sum_two_best_stats(character_spec) * 32)
    final_score = round(average_score, 2)
    if grabbable_spec["armament_type"] in character_spec["armament_types"]:
        icons.append(TYPE_MATCH_ICON)
    if final_score >= 0.3:
        icons.append(GREAT_MATCH_ICON)
    elif final_score > 0.1:
        icons.append(DECENT_MATCH_ICON)
    return icons


def get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str:
    if grabbable_spec["type"] == "armament":
        STR: str = convert_stat_to_rating("STR", grabbable_spec.get("STR", 0))
        DEX: str = convert_stat_to_rating("DEX", grabbable_spec.get("DEX", 0))
        INT: str = convert_stat_to_rating("INT", grabbable_spec.get("INT", 0))
        FAI: str = convert_stat_to_rating("FAI", grabbable_spec.get("FAI", 0))
        ARC: str = convert_stat_to_rating("ARC", grabbable_spec.get("ARC", 0))
        text = f"[{STR}|{DEX}|{INT}|{FAI}|{ARC}]"
    else:
        text = ""
    return text
