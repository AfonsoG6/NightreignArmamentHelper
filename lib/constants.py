PROGRAM_NAME = "Nightreign Armament Helper"
VERSION = "2.0.7"
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

BUTTON_TYPES = [
    CONFIRM := "confirm",
    CLOSE := "close",
]
CONTROL_TYPES = [
    KEYBOARD := "kb",
    GAMEPAD := "gp",
]
BUTTON_COORDINATES = {
    "3840x2160": {
        KEYBOARD: (1997, 1997 + 64, 97, 97 + 64),
        GAMEPAD: (2001, 2001 + 56, 101, 101 + 56),
    },
    "2560x1440": {
        KEYBOARD: (1331, 1331 + 43, 65, 65 + 42),
        GAMEPAD: (1334, 1334 + 37, 68, 68 + 36),
    },
    "1920x1080": {
        KEYBOARD: (999, 999 + 31, 49, 49 + 31),
        GAMEPAD: (1001, 1001 + 27, 51, 51 + 27),
    },
}
CONFIRM_CONTROLLER_FILENAME = "confirm_controller.png"
CONFIRM_KEYBOARD_FILENAME = "confirm_keyboard.png"

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
    CHARACTER_DETECTION: 0.90,
}
# How many pixels in the detection box must be white to even consider calling the OCR
OCR_MINIMUM_PIXELS_PERCENTS = {
    ARMAMENT_DETECTION_DEFAULT: 0.0025,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.0025,
    ARMAMENT_DETECTION_BOSS_DROP: 0.0025,
    ARMAMENT_DETECTION_SHOP: 0.0025,
    MENU_DETECTION: 0.0025,
    CHARACTER_DETECTION: 0.0025,
}
# Accepted false negative rate when matching pixel sets ((100-x)% of the white pixels must match)
PIXELSET_FN_RATES = {
    ARMAMENT_DETECTION_DEFAULT: 0.1,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.1,
    ARMAMENT_DETECTION_BOSS_DROP: 0.1,
    ARMAMENT_DETECTION_SHOP: 0.1,
    MENU_DETECTION: 0.10,
    CHARACTER_DETECTION: 0.05,
}
# Accepted false positive rate when matching pixel sets ((100-x)% of the black pixels must match)
PIXELSET_FP_RATES = {
    ARMAMENT_DETECTION_DEFAULT: 0.50,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 0.50,
    ARMAMENT_DETECTION_BOSS_DROP: 0.50,
    ARMAMENT_DETECTION_SHOP: 0.50,
    MENU_DETECTION: 0.80,
    CHARACTER_DETECTION: 0.10,
}
# Threshold from 0 - 255, higher means a cleaner image, but less info to match
PIXELSET_THRESHOLDS = {
    ARMAMENT_DETECTION_DEFAULT: 190,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 190,
    ARMAMENT_DETECTION_BOSS_DROP: 190,
    ARMAMENT_DETECTION_SHOP: 190,
    MENU_DETECTION: 200,
    CHARACTER_DETECTION: 200,
}
# Threshold reduction for comparison, higher means more lenient matching
PIXELSET_THRESHOLD_REDUCTIONS = {
    ARMAMENT_DETECTION_DEFAULT: 5,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: 5,
    ARMAMENT_DETECTION_BOSS_DROP: 5,
    ARMAMENT_DETECTION_SHOP: 5,
    MENU_DETECTION: 10,
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


UI_ELEMENT_POSITIONS = {
    # (x, y) in relative coordinates
    ARMAMENT_DETECTION_DEFAULT: (0.314, 0.2444),
    ARMAMENT_DETECTION_BOSS_DROP: (0.417, 0.2355),
    ARMAMENT_DETECTION_SHOP: (0.334, 0.22),
    CHARACTER_DROPDOWN: (0.085, 0.0944),
}


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
