PROGRAM_NAME = "Nightreign Armament Helper"
VERSION = "1.2.0"
SHOP_TITLE = "SHOP"
BOSS_DROP_TITLE = "DORMANT POWER"

TEXT_ORIGINS: list[int] = [
    TEXT_ORIGIN_NONE := 0,
    TEXT_ORIGIN_OCR := 1,
    TEXT_ORIGIN_PIXELSET := 3,
]

MATCH_RESULTS: list[int] = [
    NO_MATCH := 0,
    GOOD_MATCH := 1,
    PERFECT_MATCH := 2,
]

UI_IDENTIFIERS = [
    ARMAMENT_DETECTION_DEFAULT := "armament_detection_default",
    ARMAMENT_DETECTION_DEFAULT_REPLACE := "armament_detection_default_replace",
    ARMAMENT_DETECTION_BOSS_DROP := "armament_detection_boss_drop",
    ARMAMENT_DETECTION_SHOP := "armament_detection_shop",
    MENU_DETECTION := "menu_detection",
    CHARACTER_DETECTION := "character_detection",
    CHARACTER_DROPDOWN := "character_dropdown",
]
ARMAMENT_DETECTION_IDS = [
    ARMAMENT_DETECTION_DEFAULT,
    ARMAMENT_DETECTION_DEFAULT_REPLACE,
    ARMAMENT_DETECTION_BOSS_DROP,
    ARMAMENT_DETECTION_SHOP,
]
# Thresholds for Jaccard similarity when matching text
TEXT_SIMILARITY_THRESHOLDS = {
    ARMAMENT_DETECTION_DEFAULT: 0.85,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.85,
    ARMAMENT_DETECTION_BOSS_DROP: 0.85,
    ARMAMENT_DETECTION_SHOP: 0.85,
    MENU_DETECTION: 0.75,
    CHARACTER_DETECTION: 0.85,
}
# How many pixels in the detection box must be white to even consider calling the OCR
OCR_MINIMUM_PIXELS_PERCENTS = {
    ARMAMENT_DETECTION_DEFAULT: 0.005,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.005,
    ARMAMENT_DETECTION_BOSS_DROP: 0.005,
    ARMAMENT_DETECTION_SHOP: 0.005,
    MENU_DETECTION: 0.005,
    CHARACTER_DETECTION: 0.005,
}
# Accepted false negative rate when matching pixel sets ((100-x)% of the white pixels must match)
PIXELSET_FN_RATES = {
    ARMAMENT_DETECTION_DEFAULT: 0.075,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.075,
    ARMAMENT_DETECTION_BOSS_DROP: 0.075,
    ARMAMENT_DETECTION_SHOP: 0.075,
    MENU_DETECTION: 0.10,
    CHARACTER_DETECTION: 0.05,
}
# Accepted false positive rate when matching pixel sets ((100-x)% of the black pixels must match)
PIXELSET_FP_RATES = {
    ARMAMENT_DETECTION_DEFAULT: 0.70,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.70,
    ARMAMENT_DETECTION_BOSS_DROP: 0.70,
    ARMAMENT_DETECTION_SHOP: 0.70,
    MENU_DETECTION: 0.70,
    CHARACTER_DETECTION: 0.10,
}
# Threshold from 0 - 255, higher means a cleaner image, but less info to match
PIXELSET_THRESHOLDS = {
    ARMAMENT_DETECTION_DEFAULT: 190,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 190,
    ARMAMENT_DETECTION_BOSS_DROP: 190,
    ARMAMENT_DETECTION_SHOP: 190,
    MENU_DETECTION: 210,
    CHARACTER_DETECTION: 200,
}
# Threshold reduction for comparison, higher means more lenient matching
PIXELSET_THRESHOLD_REDUCTIONS = {
    ARMAMENT_DETECTION_DEFAULT: 10,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 10,
    ARMAMENT_DETECTION_BOSS_DROP: 10,
    ARMAMENT_DETECTION_SHOP: 10,
    MENU_DETECTION: 20,
    CHARACTER_DETECTION: 0,
}
# Time in seconds between detection checks
MINIMUM_TIME_BETWEEN_SCREENGRABS = 0.1

DETECTION_LOOP_PERIODS = {
    ARMAMENT_DETECTION_DEFAULT: 0.2,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.2,
    MENU_DETECTION: 0.5,
    CHARACTER_DETECTION: 0.2,
}

OCR_THRESHOLDS = {
    ARMAMENT_DETECTION_DEFAULT: 115,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 115,
    ARMAMENT_DETECTION_BOSS_DROP: 115,
    ARMAMENT_DETECTION_SHOP: 115,
    MENU_DETECTION: 170,
    CHARACTER_DETECTION: 140,
}

TESSERACT_CONFIG = f"--oem 3 --psm 7 -c language_model_penalty_non_freq_dict_word=1 -c language_model_penalty_non_dict_word=1 -c tessedit_do_invert=0"
TESSERACT_LANG = "eldenring"
TESSERACT_TIMEOUT = 2  # seconds

TYPE_MATCH_TEXT = "\U0001f9e4"
GREAT_MATCH_TEXT = "\u2b50"
DECENT_MATCH_TEXT = "\u2714"
NO_CHARACTER = "None"

MENU_STATES: list[str] = [
    MENU_STATE_DEFAULT := "DEFAULT",
    MENU_STATE_SHOP := SHOP_TITLE,
    MENU_STATE_BOSS_DROP := BOSS_DROP_TITLE,
]

REPLACE_ARMAMENT_REL_POS_TO_NAME = 0.3281
DETECTION_BOXES = {
    # (top, bottom, left, right)
    ARMAMENT_DETECTION_DEFAULT: (0.2833, 0.3133, 0.3800, 0.5800),
    ARMAMENT_DETECTION_DEFAULT_REPLACE: (0.2833, 0.3133, 0.3800 + REPLACE_ARMAMENT_REL_POS_TO_NAME, 0.5800 + REPLACE_ARMAMENT_REL_POS_TO_NAME),
    ARMAMENT_DETECTION_BOSS_DROP: (0.2722, 0.3055, 0.4820, 0.6820),
    ARMAMENT_DETECTION_SHOP: (0.2555, 0.2889, 0.400, 0.600),
    MENU_DETECTION: (0.1278, 0.2000, 0.0700, 0.1800),
    CHARACTER_DETECTION: (0.2000, 0.2389, 0.1250, 0.2400),
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

    # Check if the screen resolution is more wide than 16:9 or more tall than 16:9
    if (screen_width / screen_height) > (16 / 9):  # Wider than 16:9
        # Find width occupied by black bars
        black_bars_height = 0
        black_bars_width = screen_width - (screen_height * 16 / 9)
    elif (screen_width / screen_height) < (16 / 9):  # Taller than 16:9
        # Find height occupied by black bars
        black_bars_height = screen_height - (screen_width * 9 / 16)
        black_bars_width = 0
    else:  # Exactly 16:9
        black_bars_height = 0
        black_bars_width = 0
    coordinates: tuple[float, float, float, float] = DETECTION_BOXES[identifier]
    top: int = int(((screen_height - black_bars_height) * coordinates[0]) + black_bars_height / 2)
    bottom: int = int(((screen_height - black_bars_height) * coordinates[1]) + black_bars_height / 2)
    left: int = int(((screen_width - black_bars_width) * coordinates[2]) + black_bars_width / 2)
    right: int = int(((screen_width - black_bars_width) * coordinates[3]) + black_bars_width / 2)
    return top, bottom, left, right


def get_detection_box_rel(identifier: str, screen_width: int, screen_height: int) -> tuple[float, float, float, float]:
    """
    Returns the detection box coordinates in relative format based on the box name and screen resolution.
    :param identifier: Identifier for the detection box.
    :param screen_width: Width of the screen.
    :param screen_height: Height of the screen.
    :return: Tuple containing (top, bottom, left, right) coordinates of the detection box in relative format.
    """
    top, bottom, left, right = get_detection_box(identifier, screen_width, screen_height)
    return top / screen_height, bottom / screen_height, left / screen_width, right / screen_width


UI_ELEMENT_POSITIONS = {
    # (x, y) in relative coordinates
    ARMAMENT_DETECTION_DEFAULT: (0.314, 0.2444),
    ARMAMENT_DETECTION_BOSS_DROP: (0.417, 0.2355),
    ARMAMENT_DETECTION_SHOP: (0.334, 0.22),
    CHARACTER_DROPDOWN: (0.085, 0.0944),
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

    # Check if the screen resolution is more wide than 16:9 or more tall than 16:9
    if (screen_width / screen_height) > (16 / 9):  # Wider than 16:9
        # Find width occupied by black bars
        black_bars_height = 0
        black_bars_width = screen_width - (screen_height * 16 / 9)
    elif (screen_width / screen_height) < (16 / 9):  # Taller than 16:9
        # Find height occupied by black bars
        black_bars_height = screen_height - (screen_width * 9 / 16)
        black_bars_width = 0
    else:  # Exactly 16:9
        black_bars_height = 0
        black_bars_width = 0
    coordinates: tuple[float, float] = UI_ELEMENT_POSITIONS[identifier]
    x: float = (((screen_width - black_bars_width) * coordinates[0]) + black_bars_width / 2) / screen_width
    y: float = (((screen_height - black_bars_height) * coordinates[1]) + black_bars_height / 2) / screen_height
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
