# --------------------------- Imports --------------------------#
from tkinter import Tk, Toplevel, Button, Label, StringVar, OptionMenu, PhotoImage, Frame, LEFT, RIGHT, TOP, RAISED
from threading import Thread, Event, Lock
from argparse import ArgumentParser
from numpy import ndarray, array
from time import time, sleep
from os import path, makedirs
from datetime import datetime
from PIL import ImageGrab
from pytesseract import pytesseract
from cv2 import cvtColor, threshold, imwrite, COLOR_BGR2GRAY, THRESH_BINARY
from os import getenv
from traceback import format_exc
import json
import sys

# ---------------------- Project Imports -----------------------#
from lib.debug import DebugWindow
from lib.constants import *
from lib.characters import *
from lib.misc import *

# ------------------------ Constants ---------------------------#

PROGRAM_START_TIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")
if getattr(sys, "frozen", False):
    PROGRAM_DATA_PATH: str = path.join(getenv("LOCALAPPDATA", path.expanduser("~\\AppData\\Local")), PROGRAM_NAME)
    makedirs(PROGRAM_DATA_PATH, exist_ok=True)
    BASE_PATH = sys._MEIPASS
    TEMP_PATH: str = path.join(PROGRAM_DATA_PATH, "temp")
    makedirs(TEMP_PATH, exist_ok=True)
    PIXEL_SETS_PATH: str = path.join(PROGRAM_DATA_PATH, "pixel_sets")
    makedirs(PIXEL_SETS_PATH, exist_ok=True)
    ERROR_LOG_PATH: str = path.join(PROGRAM_DATA_PATH, f"error_log_{PROGRAM_START_TIME}.txt")
    CONFIG_PATH: str = path.join(PROGRAM_DATA_PATH, "config.json")
else:
    BASE_PATH = path.dirname(__file__)
    TEMP_PATH: str = path.join(BASE_PATH, "temp")
    makedirs(TEMP_PATH, exist_ok=True)
    PIXEL_SETS_PATH: str = path.join(TEMP_PATH, "pixel_sets")
    makedirs(PIXEL_SETS_PATH, exist_ok=True)
    ERROR_LOG_PATH: str = path.join(TEMP_PATH, f"error_log_{PROGRAM_START_TIME}.txt")
    CONFIG_PATH: str = path.join(TEMP_PATH, "config.json")

TESSERACT_PATH: str = path.join(BASE_PATH, "Tesseract-OCR", "tesseract.exe")
pytesseract.tesseract_cmd = TESSERACT_PATH
ICON_PATH: str = path.join(BASE_PATH, "images", "icon.png")
DEBUG: bool = False

if __name__ == "__main__":
    parser = ArgumentParser(description="Run the Elden Ring Armament Detection Tool.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()
    DEBUG = args.debug

# ---------------------- Global Variables ----------------------#

enabled: bool = True
enabled_lock: Lock = Lock()
advanced_mode_enabled: bool = False
advanced_mode_enabled_lock: Lock = Lock()
character_detection_enabled: bool = True
character_detection_enabled_lock: Lock = Lock()

enable_disable_button: Button
character_detection_button: Button
advanced_mode_button: Button
hide_show_button: Button

previous_menu_img: ndarray | None = None
previous_menu_state: str = DEFAULT_STATE
current_menu_state: str = DEFAULT_STATE
current_menu_state_lock: Lock = Lock()

previous_character_img: ndarray | None = None
previous_character_name: str = ""
current_character_name: str = ""
current_character_name_lock: Lock = Lock()

previous_armament_img: ndarray | None = None
previous_armament_name: str = ""

root: Tk
screen_width: int
screen_height: int
armament_feedback_label: Label
advanced_armament_feedback_label: Label
current_character_var: StringVar
current_character_dropdown: OptionMenu

last_menu_pixel_set: PixelSet | None = None
last_character_pixel_set: PixelSet | None = None
last_armament_pixel_set: PixelSet | None = None
pixelset_cache: PixelSetCache

# ---------------------- Functions -----------------------------#


def save_configs() -> None:
    global enabled, character_detection_enabled, advanced_mode_enabled, CONFIG_PATH, character_detection_enabled_lock, advanced_mode_enabled_lock
    with character_detection_enabled_lock, advanced_mode_enabled_lock:
        config_data = {
            "character_detection_enabled": character_detection_enabled,
            "advanced_mode_enabled": advanced_mode_enabled,
        }
    makedirs(path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config_data, config_file, indent=4)


def load_configs() -> None:
    global enabled, character_detection_enabled, advanced_mode_enabled, CONFIG_PATH, character_detection_enabled_lock, advanced_mode_enabled_lock
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config_data = json.load(config_file)
            with character_detection_enabled_lock, advanced_mode_enabled_lock:
                character_detection_enabled = config_data.get("character_detection_enabled", True)
                advanced_mode_enabled = config_data.get("advanced_mode_enabled", False)
    except (FileNotFoundError, json.JSONDecodeError):
        with character_detection_enabled_lock, advanced_mode_enabled_lock:
            character_detection_enabled = True
            advanced_mode_enabled = False
        save_configs()


def log_error(e: Exception, fatal: bool = False) -> None:
    global ERROR_LOG_PATH
    """
    Logs an error message to an error log file, that is named as the timestamp of the start of the program.
    :param e: Exception to log.
    """
    type: str = "FATAL" if fatal else "ERROR"
    makedirs(path.dirname(ERROR_LOG_PATH), exist_ok=True)

    if not path.exists(ERROR_LOG_PATH):
        open(ERROR_LOG_PATH, "w").close()

    with open(ERROR_LOG_PATH, "a") as f:
        f.write(f"[{type}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {format_exc()}\n")


def on_character_selected(e) -> None:
    global current_character_var, current_character_name, current_character_name_lock
    selected_character = current_character_var.get()
    if selected_character != NO_CHARACTER:
        with current_character_name_lock:
            current_character_name = selected_character
        update_current_character_dropdown(selected_character)
    else:
        with current_character_name_lock:
            current_character_name = ""


def quit_app() -> None:
    global root, character_detection_thread, menu_detection_thread, armament_detection_thread
    root.quit()
    character_detection_thread.stop()
    menu_detection_thread.stop()
    armament_detection_thread.stop()


def update_basic_armament_feedback_label(character_spec: CharacterSpec, armament_spec: ArmamentSpec, relx: float, rely: float) -> None:
    global armament_feedback_label
    icons: list[str] = []
    if armament_spec in character_spec.great_matches:
        icons.append(GREAT_MATCH_TEXT)
    elif armament_spec in character_spec.decent_matches:
        icons.append(DECENT_MATCH_TEXT)
    if armament_spec in character_spec.type_matches:
        icons.append(TYPE_MATCH_TEXT)
    text = "\n".join(icons) if len(icons) > 0 else ""

    armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")
    armament_feedback_label.config(text=text)


def update_advanced_armament_feedback_label(armament_spec: ArmamentSpec, relx: float, rely: float) -> None:
    global advanced_armament_feedback_label, advanced_mode_enabled, advanced_mode_enabled_lock
    STR: str = armament_spec.get_stat_letter("STR")
    DEX: str = armament_spec.get_stat_letter("DEX")
    INT: str = armament_spec.get_stat_letter("INT")
    FAI: str = armament_spec.get_stat_letter("FAI")
    ARC: str = armament_spec.get_stat_letter("ARC")
    text = f"{armament_spec.type} [{STR}|{DEX}|{INT}|{FAI}|{ARC}]"
    with advanced_mode_enabled_lock:
        if advanced_mode_enabled:
            advanced_armament_feedback_label.config(text=text)
            advanced_armament_feedback_label.place(relx=relx, rely=rely, anchor="sw")
        else:
            advanced_armament_feedback_label.config(text="")
            advanced_armament_feedback_label.place_forget()


def update_armament_feedback_labels(character_spec: CharacterSpec | None = None, armament_spec: ArmamentSpec | None = None) -> None:
    global armament_feedback_label, advanced_armament_feedback_label, screen_width, screen_height, current_menu_state, current_menu_state_lock
    if character_spec is None or armament_spec is None:
        armament_feedback_label.config(text="")
        armament_feedback_label.place_forget()
        advanced_armament_feedback_label.config(text="")
        advanced_armament_feedback_label.place_forget()
        return
    with current_menu_state_lock:
        if current_menu_state == SHOP_STATE:
            basic_relx, basic_rely = get_ui_element_rel_positions("shop_armament", screen_width, screen_height)
            advanced_rely, _, advanced_relx, _ = get_detection_box_rel("shop_armament", screen_width, screen_height)
        elif current_menu_state == BOSS_DROP_STATE:
            basic_relx, basic_rely = get_ui_element_rel_positions("boss_drop_armament", screen_width, screen_height)
            advanced_rely, _, advanced_relx, _ = get_detection_box_rel("boss_drop_armament", screen_width, screen_height)
        else:
            basic_relx, basic_rely = get_ui_element_rel_positions("default_armament", screen_width, screen_height)
            advanced_rely, _, advanced_relx, _ = get_detection_box_rel("default_armament", screen_width, screen_height)

    update_basic_armament_feedback_label(character_spec, armament_spec, basic_relx, basic_rely)
    update_advanced_armament_feedback_label(armament_spec, advanced_relx, advanced_rely)
    root.update_idletasks()


def update_current_character_dropdown(character_name: str) -> None:
    if character_name == "":
        current_character_var.set(NO_CHARACTER)
    else:
        current_character_var.set(character_name)
    root.update_idletasks()


def toggle_character_detection() -> None:
    global character_detection_enabled, character_detection_thread, character_detection_button, enabled, character_detection_enabled_lock, enabled_lock
    with enabled_lock, character_detection_enabled_lock:
        character_detection_enabled = not character_detection_enabled
        if (enabled and character_detection_enabled) and not character_detection_thread.is_alive():
            character_detection_thread = CharacterDetectionLoopThread(daemon=True)
            character_detection_thread.start()
        elif not (enabled and character_detection_enabled) and character_detection_thread.is_alive():
            character_detection_thread.stop()
        character_detection_button.config(
            text=f"{'Disable' if character_detection_enabled else 'Enable'} Character Detection",
            bg=BUTTON_ENABLED_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
            activebackground=BUTTON_ENABLED_ACTIVE_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
        )
    save_configs()


def toggle_advanced_mode() -> None:
    global advanced_mode_enabled, advanced_mode_button
    with advanced_mode_enabled_lock:
        advanced_mode_enabled = not advanced_mode_enabled
        advanced_mode_button.config(
            text=f"{'Disable' if advanced_mode_enabled else 'Enable'} Advanced Mode",
            bg=BUTTON_ENABLED_COLOR if advanced_mode_enabled else BUTTON_DISABLED_COLOR,
            activebackground=BUTTON_ENABLED_ACTIVE_COLOR if advanced_mode_enabled else BUTTON_DISABLED_ACTIVE_COLOR,
        )
    save_configs()


def toggle_enabled() -> None:
    global enabled, enable_disable_button, character_detection_thread, menu_detection_thread, armament_detection_thread, root
    with enabled_lock:
        enabled = not enabled
        if enabled:
            # Restart threads if they are not alive
            with character_detection_enabled_lock:
                if character_detection_enabled and not character_detection_thread.is_alive():
                    character_detection_thread = CharacterDetectionLoopThread(daemon=True)
                    character_detection_thread.start()
            if not menu_detection_thread.is_alive():
                menu_detection_thread = MenuDetectionLoopThread(daemon=True)
                menu_detection_thread.start()
            if not armament_detection_thread.is_alive():
                armament_detection_thread = ArmamentDetectionLoopThread(daemon=True)
                armament_detection_thread.start()
            # Show all the Overlay UI elements
            root.deiconify()
        else:
            # Stop threads
            if character_detection_thread.is_alive():
                character_detection_thread.stop()
            if menu_detection_thread.is_alive():
                menu_detection_thread.stop()
            if armament_detection_thread.is_alive():
                armament_detection_thread.stop()
            # Hide all the Overlay UI elements
            root.withdraw()
        enable_disable_button.config(
            text="Disable" if enabled else "Enable",
            bg=BUTTON_ENABLED_COLOR if enabled else BUTTON_DISABLED_COLOR,
            activebackground=BUTTON_ENABLED_ACTIVE_COLOR if enabled else BUTTON_DISABLED_COLOR,
        )
    save_configs()


def create_control_window() -> Toplevel:
    global enable_disable_button, character_detection_button, advanced_mode_button, screen_height, screen_width, control_window
    SIZE_X = 330
    SIZE_Y = 140
    BUTTON_PADDING = 2
    control_window = Toplevel()
    control_window.title(PROGRAM_NAME)
    padding_x = int(screen_width * 0.05)
    padding_y = int(screen_height * 0.15)
    control_window.geometry(f"{SIZE_X}x{SIZE_Y}+{screen_width - SIZE_X - padding_x}+{screen_height - SIZE_Y - padding_y}")
    control_window.resizable(False, False)
    icon_image = PhotoImage(file=ICON_PATH)
    control_window.iconphoto(True, icon_image)
    control_window.protocol("WM_DELETE_WINDOW", quit_app)

    top_button_frame = Frame(control_window)
    top_button_frame.pack(pady=BUTTON_PADDING)

    button_style = {
        "font": ("Arial", 12, "bold"),
        "fg": "white",
        "activeforeground": "white",
        "relief": RAISED,
        "bd": 3,
        "width": 10,
        "height": 1,
    }

    enable_disable_button = Button(
        top_button_frame,
        text="Disable" if enabled else "Enable",
        command=toggle_enabled,
        bg=BUTTON_ENABLED_COLOR if enabled else BUTTON_DISABLED_COLOR,
        activebackground=BUTTON_ENABLED_ACTIVE_COLOR if enabled else BUTTON_DISABLED_COLOR,
        **button_style,
    )
    enable_disable_button.pack(side=LEFT, padx=BUTTON_PADDING)

    quit_button = Button(top_button_frame, text="Quit", command=quit_app, bg=BUTTON_QUIT_COLOR, activebackground=BUTTON_QUIT_ACTIVE_COLOR, **button_style)
    quit_button.pack(side=LEFT, padx=BUTTON_PADDING)

    bottom_button_frame = Frame(control_window)
    bottom_button_frame.pack()

    button_style["width"] = 22

    character_detection_button = Button(
        bottom_button_frame,
        text=f"{'Disable' if character_detection_enabled else 'Enable'} Character Detection",
        command=toggle_character_detection,
        bg=BUTTON_ENABLED_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
        activebackground=BUTTON_ENABLED_ACTIVE_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
        **button_style,
    )
    character_detection_button.pack(side=TOP, pady=BUTTON_PADDING)

    advanced_mode_button = Button(
        bottom_button_frame,
        text=f"{'Disable' if advanced_mode_enabled else 'Enable'} Advanced Mode",
        command=toggle_advanced_mode,
        bg=BUTTON_ENABLED_COLOR if advanced_mode_enabled else BUTTON_DISABLED_COLOR,
        activebackground=BUTTON_ENABLED_ACTIVE_COLOR if advanced_mode_enabled else BUTTON_DISABLED_ACTIVE_COLOR,
        **button_style,
    )
    advanced_mode_button.pack(side=TOP, pady=BUTTON_PADDING)

    version_label = Label(
        control_window,
        text=f"Version {VERSION}",
        font=("Arial", 8),
        fg="gray",
        anchor="sw",
    )
    version_label.place(relx=0.01, rely=1, anchor="sw")

    return control_window


def ocr_get_character_name() -> str:
    global previous_character_img, previous_character_name, last_character_pixel_set
    img = ImageGrab.grab()

    img_np = array(img)
    gray = cvtColor(img_np, COLOR_BGR2GRAY)

    width, height = img.size
    top, bottom, left, right = get_detection_box("character", width, height)
    cropped = gray[top:bottom, left:right]

    _, img_for_ocr = threshold(cropped, 140, 255, THRESH_BINARY)
    if not image_changed(previous_character_img, cropped):
        return previous_character_name

    # To save time and resources in future detection of the same armament, we generate a pixel set
    # and check if it matches any of the previously saved pixel sets.
    pixel_set: PixelSet = PixelSet(
        pixelset_cache,
        cropped,
        width,
        height,
        "character",
        CHARACTER_PIXELSET_THRESHOLD,
        CHARACTER_PIXELSET_THRESHOLD_REDUCTION,
        CHARACTER_PIXELSET_FN_RATE,
        CHARACTER_PIXELSET_FP_RATE,
    )
    pixel_set_match = pixel_set.find_match()
    if pixel_set_match != "":
        if DEBUG:
            print(f"Armament pixel set match found: {pixel_set_match}")
        previous_character_img = img_for_ocr
        previous_character_name = pixel_set_match
        last_character_pixel_set = None
        return pixel_set_match
    if pixel_set.size() / (pixel_set.width * pixel_set.height) < OCR_MINIMUM_PIXELS_PERCENT:
        # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
        # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
        return ""
    if pixelset_cache.all_characters_learned(width, height):
        # Character detection is stable enough that we can ditch the OCR completely if we have already learned a pixel set for each character for this resolution.
        return ""
    last_character_pixel_set = pixel_set

    if DEBUG:
        debug_window.show_character_rect()
        makedirs(TEMP_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = path.join(TEMP_PATH, f"ocr_character_{timestamp}.png")
        imwrite(filename, img_for_ocr)

    text = pytesseract.image_to_string(img_for_ocr, config=TESSERACT_CONFIG, lang=TESSERACT_LANG, timeout=TESSERACT_TIMEOUT)
    if DEBUG:
        debug_window.hide_character_rect()
        print(f"Character detected: {text}")
    previous_character_img = img_for_ocr
    previous_character_name = text
    return text


def ocr_get_menu_state() -> str:
    global previous_menu_img, previous_menu_state, last_menu_pixel_set, pixelset_cache
    img = ImageGrab.grab()

    img_np = array(img)
    gray = cvtColor(img_np, COLOR_BGR2GRAY)

    width, height = img.size
    top, bottom, left, right = get_detection_box("menu_title", width, height)
    cropped = gray[top:bottom, left:right]

    _, img_for_ocr = threshold(cropped, 170, 255, THRESH_BINARY)
    if not image_changed(previous_menu_img, cropped):
        return previous_menu_state

    # To save time and resources in future detection of the same armament, we generate a pixel set
    # and check if it matches any of the previously saved pixel sets.
    pixel_set: PixelSet = PixelSet(
        pixelset_cache,
        cropped,
        width,
        height,
        "menu_title",
        MENU_PIXELSET_THRESHOLD,
        MENU_PIXELSET_THRESHOLD_REDUCTION,
        MENU_PIXELSET_FN_RATE,
        MENU_PIXELSET_FP_RATE,
    )
    pixel_set_match = pixel_set.find_match()
    if pixel_set_match != "":
        if DEBUG:
            print(f"Menu pixel set match found: {pixel_set_match}")
        previous_menu_img = img_for_ocr
        previous_menu_state = pixel_set_match
        last_menu_pixel_set = None
        return pixel_set_match
    if pixel_set.size() / (pixel_set.width * pixel_set.height) < OCR_MINIMUM_PIXELS_PERCENT:
    # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
        # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
        return DEFAULT_STATE
    last_menu_pixel_set = pixel_set

    if DEBUG:
        debug_window.show_menu_title_rect()
        makedirs(TEMP_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = path.join(TEMP_PATH, f"ocr_menu_{timestamp}.png")
        imwrite(filename, img_for_ocr)

    text = pytesseract.image_to_string(img_for_ocr, config=TESSERACT_CONFIG, lang=TESSERACT_LANG, timeout=TESSERACT_TIMEOUT)
    if DEBUG:
        debug_window.hide_menu_title_rect()
        print(f"Menu title detected: {text}")
    previous_menu_img = img_for_ocr
    previous_menu_state = text
    return text


def ocr_get_armament_name() -> str:
    global previous_armament_img, previous_armament_name, last_armament_pixel_set
    img = ImageGrab.grab()

    img_np = array(img)
    gray = cvtColor(img_np, COLOR_BGR2GRAY)

    with current_menu_state_lock:
        state = current_menu_state
    box_identifier = "default_armament"
    if state == SHOP_STATE:
        box_identifier = "shop_armament"
    elif state == BOSS_DROP_STATE:
        box_identifier = "boss_drop_armament"
    width, height = img.size
    top, bottom, left, right = get_detection_box(box_identifier, width, height)
    cropped = gray[top:bottom, left:right]

    _, img_for_ocr = threshold(cropped, 115, 255, THRESH_BINARY)
    if not image_changed(previous_armament_img, img_for_ocr):
        return previous_armament_name

    # To save time and resources in future detection of the same armament, we generate a pixel set
    # and check if it matches any of the previously saved pixel sets.
    pixel_set: PixelSet = PixelSet(
        pixelset_cache,
        cropped,
        width,
        height,
        box_identifier,
        ARMAMENT_PIXELSET_THRESHOLD,
        ARMAMENT_PIXELSET_THRESHOLD_REDUCTION,
        ARMAMENT_PIXELSET_FN_RATE,
        ARMAMENT_PIXELSET_FP_RATE,
    )
    pixel_set_match = pixel_set.find_match()
    if pixel_set_match != "":
        if DEBUG:
            print(f"Armament pixel set match found: {pixel_set_match}")
        previous_armament_img = img_for_ocr
        previous_armament_name = pixel_set_match
        last_armament_pixel_set = None
        return pixel_set_match
    if pixel_set.size() / (pixel_set.width * pixel_set.height) < OCR_MINIMUM_PIXELS_PERCENT:
        # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
        return ""
    last_armament_pixel_set = pixel_set

    if DEBUG:
        debug_window.show_armament_rect(box_identifier)
        makedirs(TEMP_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = path.join(TEMP_PATH, f"ocr_armament_{timestamp}.png")
        imwrite(filename, img_for_ocr)

    text = pytesseract.image_to_string(img_for_ocr, config=TESSERACT_CONFIG, lang=TESSERACT_LANG, timeout=TESSERACT_TIMEOUT)
    if DEBUG:
        debug_window.hide_armament_rect()
        print(f"Armament detected: {text}")
    previous_armament_img = img_for_ocr
    previous_armament_name = text
    return text


# -------------------------- Classes ---------------------------#


class MenuDetectionLoopThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def run(self) -> None:
        global current_menu_state
        while not self.is_stopped():
            t0 = time()
            try:
                text: str = ocr_get_menu_state()
                match: int = FALSE
                new_menu_state = DEFAULT_STATE
                if match := text_matches(text, SHOP_TITLE):
                    new_menu_state = SHOP_STATE
                elif match := text_matches(text, BOSS_DROP_TITLE):
                    new_menu_state = BOSS_DROP_STATE
                with current_menu_state_lock:
                    if new_menu_state != current_menu_state:
                        if DEBUG:
                            print(f"Menu state changing from '{current_menu_state}' to '{new_menu_state}'")
                        current_menu_state = new_menu_state
                        if last_menu_pixel_set and match == PERFECT and new_menu_state != DEFAULT_STATE:
                            last_menu_pixel_set.write(new_menu_state)
            except Exception as e:
                log_error(e)
            t1 = time()
            sleep_time = max(0, MENU_DETECTION_LOOP_PERIOD - (t1 - t0))
            sleep(sleep_time)

    def stop(self) -> None:
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


class ArmamentDetectionLoopThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def run(self) -> None:
        global current_menu_state, thread_running, current_character_name
        while not self.is_stopped():
            t0 = time()
            try:
                with current_character_name_lock:
                    character_spec: CharacterSpec | None = CHARACTER_SPECS.get(current_character_name, None)
                if character_spec is not None:
                    text = ocr_get_armament_name()
                    for armament_spec in ARMAMENT_SPECS:
                        if match := text_matches(text, armament_spec.name):
                            if DEBUG:
                                print(f"Armament match found: {armament_spec.name} ({text})")
                            update_armament_feedback_labels(character_spec, armament_spec)
                            if last_armament_pixel_set and match == PERFECT:
                                last_armament_pixel_set.write(armament_spec.name)
                            break
                    else:  # No match found
                        update_armament_feedback_labels()
            except Exception as e:
                log_error(e)
            t1 = time()
            sleep_time = max(0, ARMAMENT_DETECTION_LOOP_PERIOD - (t1 - t0))
            sleep(sleep_time)

    def stop(self) -> None:
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


class CharacterDetectionLoopThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def run(self) -> None:
        global current_character_name, current_character_name_lock, character_detection_enabled, current_character_name_lock
        if DEBUG:
            print("Starting character detection thread.")
        while not self.is_stopped():
            t0 = time()
            try:
                with current_character_name_lock:
                    do_character_detection: bool = character_detection_enabled
                if do_character_detection:
                    text: str = ocr_get_character_name()
                    match: int = FALSE
                    for char in CHARACTERS:
                        if match := text_matches(text, char):
                            new_character_name = char
                            break
                    else:  # No match found
                        new_character_name = ""
                    with current_character_name_lock:
                        if new_character_name != "" and new_character_name != current_character_name:
                            current_character_name = new_character_name
                            update_current_character_dropdown(new_character_name)
                            if last_character_pixel_set and match == PERFECT:
                                last_character_pixel_set.write(new_character_name)
            except Exception as e:
                log_error(e)
            t1 = time()
            sleep_time = max(0, CHARACTER_DETECTION_LOOP_PERIOD - (t1 - t0))
            sleep(sleep_time)
        if DEBUG:
            print("Character detection thread stopped.")

    def stop(self) -> None:
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


# -------------------------- Main ------------------------------#


if __name__ == "__main__":
    load_configs()
    
    root = Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")
    icon_image = PhotoImage(file=ICON_PATH)
    root.iconphoto(True, icon_image)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.config(bg="black")
    root.withdraw()

    basic_armament_feedback_label_font_size = int(screen_height * 0.014)
    advanced_armament_feedback_label_font_size = int(screen_height * 0.012)
    current_character_label_font_size = int(screen_height * 0.008)

    armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Arial", basic_armament_feedback_label_font_size))
    armament_feedback_label.pack()
    relx, rely = get_ui_element_rel_positions("default_armament", screen_width, screen_height)
    armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")

    advanced_armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Consolas", advanced_armament_feedback_label_font_size))
    advanced_armament_feedback_label.pack()
    rely, _, relx, _ = get_detection_box("default_armament", screen_width, screen_height)
    advanced_armament_feedback_label.place(relx=relx, rely=rely + ADVANCED_FEEDBACK_RELPOSTONAME, anchor="nw")

    current_character_var = StringVar(value=NO_CHARACTER)

    current_character_dropdown = OptionMenu(root, current_character_var, *CHARACTERS, command=on_character_selected)
    current_character_dropdown.config(bg="black", fg="white", font=("Arial", current_character_label_font_size), bd=0, highlightthickness=0)
    current_character_dropdown["menu"].config(bg="black", fg="white", font=("Arial", current_character_label_font_size))
    relx, rely = get_ui_element_rel_positions("character_dropdown", screen_width, screen_height)
    current_character_dropdown.place(relx=relx, rely=rely, anchor="ne")

    character_detection_thread = CharacterDetectionLoopThread(daemon=True)
    menu_detection_thread = MenuDetectionLoopThread(daemon=True)
    armament_detection_thread = ArmamentDetectionLoopThread(daemon=True)
    if DEBUG:
        debug_window = DebugWindow(root)

    calculate_all_armaments()
    pixelset_cache = PixelSetCache(PIXEL_SETS_PATH, DEBUG)
    update_armament_feedback_labels()
    update_current_character_dropdown(current_character_name)
    control_window = create_control_window()
    try:
        root.deiconify()
        do_start: bool
        with character_detection_enabled_lock:
            do_start = character_detection_enabled
        if do_start:
            character_detection_thread.start()
        menu_detection_thread.start()
        armament_detection_thread.start()
        print("Ready!")
        root.mainloop()
    except Exception as e:
        log_error(e, True)
    except KeyboardInterrupt:
        print("Manual program stop.")
        quit_app()
