character_tiers = {
    "S": 100,
    "A": 80,
    "B": 60,
    "C": 40,
    "D": 20,
    "E": 0,
}

overall_tier = {
    6: "SS",
    5: "S",
    4: "A",
    3: "B",
    2: "C",
    1: "D",
    0: "E",
}

TIER_INCREMENT = 15
MAX_TIER = 6

TYPE_MATCH_ICON = "\U0001f9e4"


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


def get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str:
    if grabbable_spec["type"] == "armament":
        total = 0
        for att in ["STR", "DEX", "INT", "FAI", "ARC"]:
            chr = character_tiers[character_spec[att]]
            wep = grabbable_spec[att]
            total += (chr * wep) / 100
        num_tier = min(round(total / TIER_INCREMENT), MAX_TIER)
        dec_tier = min((total / TIER_INCREMENT), MAX_TIER) - num_tier
        letter = overall_tier[num_tier]
        if dec_tier <= -0.25:
            letter += "-"
        elif dec_tier >= 0.25:
            letter += "+"
        rounded_total = round(total, 1)
        STR: str = convert_stat_to_rating("STR", grabbable_spec.get("STR", 0))
        DEX: str = convert_stat_to_rating("DEX", grabbable_spec.get("DEX", 0))
        INT: str = convert_stat_to_rating("INT", grabbable_spec.get("INT", 0))
        FAI: str = convert_stat_to_rating("FAI", grabbable_spec.get("FAI", 0))
        ARC: str = convert_stat_to_rating("ARC", grabbable_spec.get("ARC", 0))
        return f"{letter} ( {rounded_total}% ) [{STR}|{DEX}|{INT}|{FAI}|{ARC}]"
    return ""


def get_basic_label_icons(character_spec: dict, grabbable_spec: dict) -> list[str]:
    icons: list[str] = []
    if grabbable_spec["type"] != "armament":
        return []

    if grabbable_spec["armament_type"] in character_spec["armament_types"]:
        icons.append(TYPE_MATCH_ICON)

    return icons
