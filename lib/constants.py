SHOP_TITLE_WORDS = ["SHOP"]
BOSS_DROP_TITLE_WORDS = ["DORMANT POWER"]
ARMAMENT_TEXT_DISTANCE_THRESHOLD = 0.75  # Relative distance threshold for armament text detection
# Time in seconds between detection checks
MENU_DETECTION_LOOP_PERIOD = 0.01
ARMAMENT_DETECTION_LOOP_PERIOD = 0.01
CHARACTER_DETECTION_LOOP_PERIOD = 0.01

TESSERACT_CONFIG = f"--oem 3 --psm 7 -c language_model_penalty_non_freq_dict_word=1 -c language_model_penalty_non_dict_word=1"
TESSERACT_LANG = "eldenring"

TYPE_MATCH_TEXT = "🧤"
GREAT_MATCH_TEXT = "⭐"
DECENT_MATCH_TEXT = "✔️"
NO_CHARACTER = "None"

ITEM_HELPER_STATES = [
    DEFAULT_STATE := 0,
    SHOP_STATE := 1,
    BOSS_DROP_STATE := 2,
]

DETECTION_BOXES = {
    # (top, bottom, left, right)
    "default_armament": {
        "resolution": (16, 10),
        "coordinates": (0.305, 0.332, 0.38, 0.62),
    },
    "boss_drop_armament": {
        "resolution": (16, 10),
        "coordinates": (0.295, 0.325, 0.482, 0.71),
    },
    "shop_armament": {
        "resolution": (16, 10),
        "coordinates": (0.28, 0.31, 0.4, 0.65),
    },
    "menu_title": {
        "resolution": (16, 10),
        "coordinates": (0.165, 0.23, 0.07, 0.18),
    },
    "character": {
        "resolution": (16, 10),
        "coordinates": (0.23, 0.265, 0.125, 0.24),
    },
}


def get_detection_box(identifier: str, screen_width: int, screen_height: int) -> tuple[int, int, int, int]:
    """
    Returns the detection box coordinates based on the box name and screen resolution.
    :param identifier: Identifier for the detection box.
    :param screen_width: Width of the screen.
    :param screen_height: Height of the screen.
    :return: Tuple containing (top, bottom, left, right) coordinates of the detection box.
    """

    if identifier not in DETECTION_BOXES:
        raise ValueError(f"Invalid detection box name: {identifier}")

    # Convert the coordinates from the reference resolution to the current screen resolution
    ref_resolution: tuple[int, int] = DETECTION_BOXES[identifier]["resolution"]
    tgt_resolution: tuple[float, float]
    # Check if the screen resolution is more wide than 16:9 or more tall than 16:9
    if (screen_width / screen_height) > (16 / 9):  # Wider than 16:9
        tgt_resolution = ((screen_width / screen_height) * 9, 9)
    else:  # Taller than 16:9
        tgt_resolution = (16, (screen_height / screen_width) * 16)
    coordinates: tuple[float, float, float, float] = DETECTION_BOXES[identifier]["coordinates"]
    top: int = int(screen_height * (coordinates[0] * tgt_resolution[1] / ref_resolution[1]))
    bottom: int = int(screen_height * (coordinates[1] * tgt_resolution[1] / ref_resolution[1]))
    left: int = int(screen_width * (coordinates[2] * tgt_resolution[0] / ref_resolution[0]))
    right: int = int(screen_width * (coordinates[3] * tgt_resolution[0] / ref_resolution[0]))
    return top, bottom, left, right


UI_ELEMENT_POSITIONS = {
    # (x, y) in relative coordinates
    "default_armament": {
        "resolution": (16, 10),
        "coordinates": (0.314, 0.27),
    },
    "boss_drop_armament": {
        "resolution": (16, 10),
        "coordinates": (0.417, 0.262),
    },
    "shop_armament": {
        "resolution": (16, 10),
        "coordinates": (0.334, 0.248),
    },
    "character_dropdown": {
        "resolution": (16, 10),
        "coordinates": (0.085, 0.135),
    },
}


def get_ui_element_rel_positions(identifier: str, screen_width: int, screen_height: int) -> tuple[float, float]:
    """
    Returns the coordinates of a UI element based on its identifier and screen resolution.
    :param identifier: Identifier for the UI element.
    :param screen_width: Width of the screen.
    :param screen_height: Height of the screen.
    :return: Tuple containing (x, y) coordinates of the UI element.
    """

    if identifier not in UI_ELEMENT_POSITIONS:
        raise ValueError(f"Invalid item feedback identifier: {identifier}")

    # Convert the coordinates from the reference resolution to the current screen resolution
    ref_resolution: tuple[int, int] = UI_ELEMENT_POSITIONS[identifier]["resolution"]
    tgt_resolution: tuple[float, float]
    # Check if the screen resolution is more wide than 16:9 or more tall than 16:9
    if screen_width / screen_height > 16 / 9:  # Wider than 16:9
        tgt_resolution = ((screen_width / screen_height) * 9, 9)
    else:  # Taller than 16:9
        tgt_resolution = (16, (screen_height / screen_width) * 16)
    coordinates: tuple[float, float] = UI_ELEMENT_POSITIONS[identifier]["coordinates"]
    x: float = coordinates[0] * tgt_resolution[0] / ref_resolution[0]
    y: float = coordinates[1] * tgt_resolution[1] / ref_resolution[1]
    return x, y


# Button Colors
BUTTON_ENABLED_COLOR = "#4CAF50"  # Green
BUTTON_ENABLED_ACTIVE_COLOR = "#45A049"  # Darker green
BUTTON_DISABLED_COLOR = "#F44336"  # Red
BUTTON_DISABLED_ACTIVE_COLOR = "#D32F2F"  # Darker red
BUTTON_QUIT_COLOR = "#40627C"  # Moonlight blue
BUTTON_QUIT_ACTIVE_COLOR = "#304A5C"  # Darker blue

CHARACTERS = [
    WYLDER := "WYLDER",
    GUARDIAN := "GUARDIAN",
    IRONEYE := "IRONEYE",
    DUCHESS := "DUCHESS",
    RAIDER := "RAIDER",
    REVENANT := "REVENANT",
    RECLUSE := "RECLUSE",
    EXECUTOR := "EXECUTOR",
]

WEAPON_TYPES = [
    DAGGER := "Dagger",
    STRAIGHT_SWORD := "Straight Sword",
    GREATSWORD := "Greatsword",
    COLOSSAL_SWORD := "Colossal Sword",
    THRUSTING_SWORD := "Thrusting Sword",
    HEAVY_THRUSTING_SWORD := "Heavy Thrusting Sword",
    CURVED_SWORD := "Curved Sword",
    CURVED_GREATSWORD := "Curved Greatsword",
    KATANA := "Katana",
    TWINBLADE := "Twinblade",
    AXE := "Axe",
    GREATAXE := "Greataxe",
    HAMMER := "Hammer",
    FLAILS := "Flails",
    GREAT_HAMMER := "Great Hammer",
    COLOSSAL_WEAPON := "Colossal Weapon",
    SPEAR := "Spear",
    GREAT_SPEAR := "Great Spear",
    HALBERD := "Halberd",
    REAPER := "Reaper",
    WHIP := "Whip",
    FIST := "Fist",
    CLAWS := "Claws",
    BOW := "Bow",
    GREATBOW := "Great Bow",
    CROSSBOW := "Crossbow",
    BALLISTA := "Ballista",
    TORCH := "Torch",
    SMALL_SHIELD := "Small Shield",
    MEDIUM_SHIELD := "Medium Shield",
    GREATSHIELD := "Greatshield",
    GLINTSTONE_STAFF := "Glintstone Staff",
    SACRED_SEAL := "Sacred Seal",
]

AFFINITIES = [
    FIRE := "Fire",
    MAGIC := "Magic",
    HOLY := "Holy",
    LIGHTNING := "Lightning",
    BLEED := "Bleed",
    POISON := "Poison",
    SCARLET_ROT := "Scarlet Rot",
    FROSTBITE := "Frostbite",
    SLEEP := "Sleep",
    MADNESS := "Madness",
]
