from lib.constants import *
from lib.armaments import *

RATINGS: list[int] = [
    S := 32,
    A := 16,
    B := 8,
    C := 4,
    D := 2,
    E := 1,
    _ := 0,
]


class CharacterSpec:
    """
    Class representing a character specification.
    """

    def __init__(self, name: str, weapon_types: list[str], STR: int, DEX: int, INT: int, FAI: int, ARC: int):
        self.name: str = name
        self.weapon_types: list[str] = weapon_types
        self.STR: int = STR
        self.DEX: int = DEX
        self.INT: int = INT
        self.FAI: int = FAI
        self.ARC: int = ARC
        self.type_matches: list[ArmamentSpec] = []
        self.great_matches: list[ArmamentSpec] = []
        self.decent_matches: list[ArmamentSpec] = []

    def calculate_armaments(self):
        self.type_matches = []
        self.great_matches = []
        self.decent_matches = []

        for armament_spec in ARMAMENT_SPECS:
            if armament_spec.type in self.weapon_types:
                self.type_matches.append(armament_spec)
            stat_score = calculate_stat_score(armament_spec, self)
            if stat_score >= 0.3:
                self.great_matches.append(armament_spec)
            elif stat_score > 0.1:
                self.decent_matches.append(armament_spec)

    def get_highest_rating(self) -> int:
        """
        Returns the highest rating among the character's stats.
        """
        return max(self.STR, self.DEX, self.INT, self.FAI, self.ARC)

    def get_sum_stats(self) -> int:
        """
        Returns the sum of the character's stats.
        """
        return self.STR + self.DEX + self.INT + self.FAI + self.ARC

    def get_sum_two_best_stats(self) -> int:
        """
        Returns the sum of the two highest stats of the character.
        """
        stats: list[int] = [self.STR, self.DEX, self.INT, self.FAI, self.ARC]
        stats.sort(reverse=True)
        return stats[0] + stats[1]


# Changed DEX from B to A for DUCHESS due to the real stats actually being 1 point apart.
CHARACTER_SPECS: dict[str, CharacterSpec] = {
    WYLDER: CharacterSpec(WYLDER, [GREATSWORD], A, B, C, C, C),
    GUARDIAN: CharacterSpec(GUARDIAN, [HALBERD, GREATSHIELD], B, C, D, C, C),
    IRONEYE: CharacterSpec(IRONEYE, [BOW], C, A, D, D, B),
    DUCHESS: CharacterSpec(DUCHESS, [DAGGER], D, A, A, B, D),
    RAIDER: CharacterSpec(RAIDER, [GREATAXE, GREAT_HAMMER, COLOSSAL_WEAPON], S, C, D, D, C),
    REVENANT: CharacterSpec(REVENANT, [], C, C, B, S, B),
    RECLUSE: CharacterSpec(RECLUSE, [], D, C, S, S, C),
    EXECUTOR: CharacterSpec(EXECUTOR, [KATANA], C, S, D, D, S),
}


def calculate_stat_score(armament_spec: ArmamentSpec, character_spec: CharacterSpec) -> float:
    """
    Calculates the score of an armament's stats when compared with a character's stats.
    """
    score: int = 0
    stats: list[str] = ["STR", "DEX", "INT", "FAI", "ARC"]
    for stat in stats:
        armament_stat: int = getattr(armament_spec, stat)
        character_stat: int = getattr(character_spec, stat)
        if armament_stat == _:
            continue
        score += armament_stat * character_stat
    average_score: float = score / (character_spec.get_sum_two_best_stats() * S)
    return round(average_score, 2)


def calculate_all_armaments():
    """
    Calculates the best armaments for each character based on their stats and weapon preferences.
    Returns a dictionary with character names as keys and their best armaments as values.
    This should be called only once at the start of the program to populate the matches.
    """
    for _, character_spec in CHARACTER_SPECS.items():
        character_spec.calculate_armaments()

"""
# This block is for debugging purposes to generate a JSON file with matches for each character.
import json
if __name__ == "__main__":
    out_object = {}
    calculate_all_armaments()
    for character_name, character_spec in CHARACTER_SPECS.items():
        out_object[character_name] = {
            "type_matches": [f"{armament.name} ({armament.get_best_stat()})" for armament in character_spec.type_matches],
            "great_matches": [f"{armament.name} ({armament.get_best_stat()})" for armament in character_spec.great_matches],
            "decent_matches": [f"{armament.name} ({armament.get_best_stat()})" for armament in character_spec.decent_matches],
        }

    with open("debug_matches.json", "w") as f:
        json.dump(out_object, f, indent=4)
"""