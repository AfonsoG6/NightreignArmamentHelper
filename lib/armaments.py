from lib.constants import *
import json

RATINGS: list[int] = [
    S := 32,
    A := 16,
    B := 8,
    C := 4,
    D := 2,
    E := 1,
    _ := 0,
]


class ArmamentSpec:
    """
    Class representing an armament specification.
    """

    def __init__(self, id: int, name: str, type: str, STR: int, DEX: int, INT: int, FAI: int, ARC: int):
        self.id: int = id
        self.name: str = name
        self.type: str = type
        self.STR: int = self.convert_stat_to_rating("STR", STR)
        self.DEX: int = self.convert_stat_to_rating("DEX", DEX)
        self.INT: int = self.convert_stat_to_rating("INT", INT)
        self.FAI: int = self.convert_stat_to_rating("FAI", FAI)
        self.ARC: int = self.convert_stat_to_rating("ARC", ARC)

    def convert_stat_to_rating(self, stat_name: str, stat_value: int) -> int:
        if stat_value == 0:
            return _
        if stat_name in ["STR", "DEX"]:
            if stat_value < 15:
                return E
            elif stat_value < 30:
                return D
            elif stat_value < 45:
                return C
            elif stat_value < 60:
                return B
            elif stat_value < 75:
                return A
            else:
                return S
        elif stat_name in ["INT", "FAI"]:
            if stat_value < 20:
                return E
            elif stat_value < 30:
                return D
            elif stat_value < 40:
                return C
            elif stat_value < 50:
                return B
            elif stat_value < 60:
                return A
            else:
                return S
        elif stat_name == "ARC":
            if stat_value < 10:
                return E
            elif stat_value < 20:
                return D
            elif stat_value < 40:
                return C
            elif stat_value < 60:
                return B
            elif stat_value < 80: 
                return A
            else:
                return S
        return _

    def get_best_stat(self) -> str:
        """
        Returns the name of the stat with the highest rating.
        """
        best_stat: int = max(self.STR, self.DEX, self.INT, self.FAI, self.ARC)
        res: list[str] = []
        if best_stat == self.STR:
            res.append("STR")
        if best_stat == self.DEX:
            res.append("DEX")
        if best_stat == self.INT:
            res.append("INT")
        if best_stat == self.FAI:
            res.append("FAI")
        if best_stat == self.ARC:
            res.append("ARC")
        return ", ".join(res)

    def get_stat_rating_text(self, stat_id: str) -> str:
        stat_value: int = getattr(self, stat_id)
        if stat_value == S:
            return "S"
        elif stat_value == A:
            return "A"
        elif stat_value == B:
            return "B"
        elif stat_value == C:
            return "C"
        elif stat_value == D:
            return "D"
        elif stat_value == E:
            return "E"
        else:
            return "-"

ARMAMENT_SPECS: set[ArmamentSpec] = set()

def load_all_armament_specs(json_path: str) -> None:
    global ARMAMENT_SPECS
    with open(json_path, 'r', encoding='utf-8') as file:
        armament_data = json.load(file)
        for armament in armament_data:
            ARMAMENT_SPECS.add(ArmamentSpec(
                id=armament['id'],
                name=armament['name'],
                type=armament['type'],
                STR=armament['STR'],
                DEX=armament['DEX'],
                INT=armament['INT'],
                FAI=armament['FAI'],
                ARC=armament['ARC']
            ))


def find_armament_name_by_id(armament_id: int) -> str:
    for armament in ARMAMENT_SPECS:
        if armament.id == armament_id:
            return armament.name
    return ""