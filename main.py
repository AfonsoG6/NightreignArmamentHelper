# --------------------------- Imports --------------------------#
from tkinter import Tk, Toplevel, Button, Label, StringVar, OptionMenu, PhotoImage, Frame, LEFT, TOP, RAISED
from threading import Thread, Event, Lock
from argparse import ArgumentParser
from traceback import format_exc
from numpy import ndarray, array
from time import time, sleep
from os import path, makedirs
from shutil import rmtree
from datetime import datetime
from PIL import ImageGrab
from pytesseract import pytesseract
from cv2 import cvtColor, threshold, bitwise_and, resize, COLOR_BGR2GRAY, THRESH_BINARY_INV, INTER_AREA
from inspect import getfullargspec
from os import getenv
import json
import sys

# ---------------------- Project Imports -----------------------#
from lib.debug import DebugWindow
from lib.constants import *
from lib.characters import *
from lib.default_extension import *
from lib.misc import *

# ------------------------ Constants ---------------------------#

PROGRAM_START_TIME: str = datetime.now().strftime("%Y%m%d_%H%M%S")
if getattr(sys, "frozen", False):
    BASE_PATH = sys._MEIPASS  # type: ignore
    PROGRAM_DATA_PATH: str = path.join(getenv("LOCALAPPDATA", path.expanduser("~\\AppData\\Local")), PROGRAM_NAME)
else:
    BASE_PATH = path.dirname(__file__)
    PROGRAM_DATA_PATH: str = path.join(BASE_PATH, "temp")

PIXEL_SETS_PATH: str = path.join(PROGRAM_DATA_PATH, "pixel_sets")
DEBUG_PATH: str = path.join(PROGRAM_DATA_PATH, "debug")
RESOURCES_PATH: str = path.join(BASE_PATH, "resources")

EXTENSIONS_PATH: str = path.join(PROGRAM_DATA_PATH, "extensions")
CONFIG_PATH: str = path.join(PROGRAM_DATA_PATH, "config.json")
ERROR_LOG_PATH: str = path.join(PROGRAM_DATA_PATH, f"error_log_{PROGRAM_START_TIME}.txt")

TESSERACT_PATH: str = path.join(RESOURCES_PATH, "Tesseract-OCR", "tesseract.exe")
ICON_PATH: str = path.join(RESOURCES_PATH, "icon.png")

pytesseract.tesseract_cmd = TESSERACT_PATH
TESSDATA_PREFIX = path.join(RESOURCES_PATH, "Tesseract-OCR", "tessdata")
pytesseract.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX

DEBUG: bool = False
if __name__ == "__main__":
    parser = ArgumentParser(description="Run Nightreign Armament Helper Overlay.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()
    DEBUG = args.debug

# ---------------------- Global Variables ----------------------#

enabled: bool = True
enabled_lock: Lock = Lock()
enable_disable_button: Button

character_detection_enabled: bool = True
character_detection_enabled_lock: Lock = Lock()
character_detection_button: Button

advanced_mode_enabled: bool = False
advanced_mode_enabled_lock: Lock = Lock()
advanced_mode_button: Button

current_menu_state: str = MENU_STATE_DEFAULT
current_menu_state_lock: Lock = Lock()
current_character_name: str = ""
current_character_name_lock: Lock = Lock()

previous_imgs_lock: Lock = Lock()
previous_imgs: dict[str, ndarray | None] = {
    ARMAMENT_DETECTION_DEFAULT: None,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: None,
    ARMAMENT_DETECTION_BOSS_DROP: None,
    ARMAMENT_DETECTION_SHOP: None,
    MENU_DETECTION: None,
    CHARACTER_DETECTION: None,
}

previous_matches_lock: Lock = Lock()
previous_matches: dict[str, tuple[int, str]] = {
    ARMAMENT_DETECTION_DEFAULT: (TEXT_ORIGIN_NONE, ""),
    ARMAMENT_DETECTION_DEFAULT_REPLACE: (TEXT_ORIGIN_NONE, ""),
    ARMAMENT_DETECTION_BOSS_DROP: (TEXT_ORIGIN_NONE, ""),
    ARMAMENT_DETECTION_SHOP: (TEXT_ORIGIN_NONE, ""),
    MENU_DETECTION: (TEXT_ORIGIN_NONE, ""),
    CHARACTER_DETECTION: (TEXT_ORIGIN_NONE, ""),
}

last_pixelsets_lock: Lock = Lock()
last_pixelsets: dict[str, PixelSet | None] = {
    ARMAMENT_DETECTION_DEFAULT: None,
    ARMAMENT_DETECTION_DEFAULT_REPLACE: None,
    ARMAMENT_DETECTION_BOSS_DROP: None,
    ARMAMENT_DETECTION_SHOP: None,
    MENU_DETECTION: None,
    CHARACTER_DETECTION: None,
}

root: Tk
screen_width_ui: int
screen_height_ui: int
screen_width_real: int
screen_height_real: int
basic_armament_feedback_label: Label
advanced_armament_feedback_label: Label
replace_basic_armament_feedback_label: Label
replace_advanced_armament_feedback_label: Label
current_character_var: StringVar
current_character_dropdown: OptionMenu

last_screengrab: Image.Image | None = None
last_screengrab_time: float = 0.0
screengrab_lock: Lock = Lock()
pixelset_cache: PixelSetCache
button_detection_required: bool = False
image_cache: ImageCache = ImageCache()

extension_load_mode: str = ""
loaded_extensions: dict[str, list[str]]

# ---------------------- Functions -----------------------------#


def save_configs() -> None:
    global enabled, character_detection_enabled, advanced_mode_enabled, CONFIG_PATH, character_detection_enabled_lock, advanced_mode_enabled_lock
    with character_detection_enabled_lock, advanced_mode_enabled_lock:
        config_data = {
            "version": VERSION,
            "character_detection_enabled": character_detection_enabled,
            "advanced_mode_enabled": advanced_mode_enabled,
        }
    makedirs(PROGRAM_DATA_PATH, exist_ok=True)
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
                data_version = config_data.get("version", "0.0.0")
                if version_is_older(data_version, "2.0.1"):
                    rmtree(PIXEL_SETS_PATH, ignore_errors=True)
            if data_version != VERSION:
                save_configs()
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
    makedirs(PROGRAM_DATA_PATH, exist_ok=True)

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
    global root, character_detection_thread, menu_detection_thread, armament_detection_thread, replace_armament_detection_thread
    root.quit()
    character_detection_thread.stop()
    menu_detection_thread.stop()
    armament_detection_thread.stop()
    replace_armament_detection_thread.stop()


def get_current_character_spec() -> dict | None:
    global current_character_name, current_character_name_lock
    with current_character_name_lock:
        character_name = current_character_name
    if character_name == NO_CHARACTER or character_name == "":
        return None
    for character_spec in CHARACTER_SPECS:
        if character_spec["name"] == character_name:
            return character_spec
    return None


def call_get_basic_label_icons(character_spec: dict, grabbable_spec: dict) -> list[str]:
    global loaded_extensions, extension_load_mode
    icons: list[str] = []
    if extension_load_mode == LOAD_MODE_AFTER:
        icons.extend(get_basic_label_icons(character_spec, grabbable_spec))
    if "get_basic_label_icons" in loaded_extensions:
        for module_name in loaded_extensions["get_basic_label_icons"]:
            module = sys.modules.get(module_name)
            if module and hasattr(module, "get_basic_label_icons"):
                result = module.get_basic_label_icons(character_spec, grabbable_spec)
                if isinstance(result, list):
                    icons.extend(result)
        if extension_load_mode == LOAD_MODE_OVERRIDE:
            return icons
    if extension_load_mode == LOAD_MODE_BEFORE or extension_load_mode == "":
        icons.extend(get_basic_label_icons(character_spec, grabbable_spec))
    return icons


def call_get_advanced_label_text(character_spec: dict, grabbable_spec: dict) -> str:
    global loaded_extensions, extension_load_mode
    text = ""
    if extension_load_mode == LOAD_MODE_AFTER:
        text += get_advanced_label_text(character_spec, grabbable_spec)
    if "get_advanced_label_text" in loaded_extensions:
        for module_name in loaded_extensions["get_advanced_label_text"]:
            module = sys.modules.get(module_name)
            if module and hasattr(module, "get_advanced_label_text"):
                result = module.get_advanced_label_text(character_spec, grabbable_spec)
                if isinstance(result, str):
                    text += result
        return text
    if extension_load_mode == LOAD_MODE_BEFORE or extension_load_mode == "":
        text += get_advanced_label_text(character_spec, grabbable_spec)
    return text


def update_basic_armament_feedback_label(character_spec: dict, grabbable_spec: dict, relx: float, rely: float) -> None:
    global basic_armament_feedback_label
    icons: list[str] = call_get_basic_label_icons(character_spec, grabbable_spec)
    text = "\n".join(icons) if len(icons) > 0 else ""

    basic_armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")
    basic_armament_feedback_label.config(text=text)


def update_advanced_armament_feedback_label(character_spec: dict, grabbable_spec: dict, relx: float, rely: float) -> None:
    global advanced_armament_feedback_label, advanced_mode_enabled, advanced_mode_enabled_lock
    text = call_get_advanced_label_text(character_spec, grabbable_spec)
    with advanced_mode_enabled_lock:
        if advanced_mode_enabled:
            advanced_armament_feedback_label.config(text=text)
            advanced_armament_feedback_label.place(relx=relx, rely=rely, anchor="sw")
        else:
            advanced_armament_feedback_label.config(text="")
            advanced_armament_feedback_label.place_forget()


def update_armament_feedback_labels(character_spec: dict | None = None, grabbable_spec: dict | None = None) -> None:
    global basic_armament_feedback_label, advanced_armament_feedback_label, screen_width_ui, screen_height_ui, current_menu_state, current_menu_state_lock
    if character_spec is None or grabbable_spec is None:
        basic_armament_feedback_label.config(text="")
        basic_armament_feedback_label.place_forget()
        advanced_armament_feedback_label.config(text="")
        advanced_armament_feedback_label.place_forget()
        return
    with current_menu_state_lock:
        if current_menu_state == MENU_STATE_SHOP:
            basic_relx, basic_rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_SHOP, screen_width_ui, screen_height_ui)
            advanced_rely, _, advanced_relx, _ = get_detection_box_coordinates_rel(ARMAMENT_DETECTION_SHOP, screen_width_ui, screen_height_ui)
        elif current_menu_state == MENU_STATE_BOSS_DROP:
            basic_relx, basic_rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_BOSS_DROP, screen_width_ui, screen_height_ui)
            advanced_rely, _, advanced_relx, _ = get_detection_box_coordinates_rel(ARMAMENT_DETECTION_BOSS_DROP, screen_width_ui, screen_height_ui)
        else:
            basic_relx, basic_rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
            advanced_rely, _, advanced_relx, _ = get_detection_box_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)

    update_basic_armament_feedback_label(character_spec, grabbable_spec, basic_relx, basic_rely)
    update_advanced_armament_feedback_label(character_spec, grabbable_spec, advanced_relx, advanced_rely)
    root.update_idletasks()


def update_armament_feedback_labels_general(detection_id: str, character_spec: dict | None = None, grabbable_spec: dict | None = None) -> None:
    if detection_id == ARMAMENT_DETECTION_DEFAULT:
        update_armament_feedback_labels(character_spec, grabbable_spec)
    elif detection_id == ARMAMENT_DETECTION_DEFAULT_REPLACE:
        update_replace_armament_feedback_labels(character_spec, grabbable_spec)


def update_replace_basic_armament_feedback_label(character_spec: dict, grabbable_spec: dict, relx: float, rely: float) -> None:
    global replace_basic_armament_feedback_label
    icons: list[str] = call_get_basic_label_icons(character_spec, grabbable_spec)
    text = "\n".join(icons) if len(icons) > 0 else ""

    replace_basic_armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")
    replace_basic_armament_feedback_label.config(text=text)


def update_replace_advanced_armament_feedback_label(character_spec: dict, grabbable_spec: dict, relx: float, rely: float) -> None:
    global replace_advanced_armament_feedback_label, advanced_mode_enabled, advanced_mode_enabled_lock
    text = call_get_advanced_label_text(character_spec, grabbable_spec)
    with advanced_mode_enabled_lock:
        if advanced_mode_enabled:
            replace_advanced_armament_feedback_label.config(text=text)
            replace_advanced_armament_feedback_label.place(relx=relx, rely=rely, anchor="sw")
        else:
            replace_advanced_armament_feedback_label.config(text="")
            replace_advanced_armament_feedback_label.place_forget()


def update_replace_armament_feedback_labels(character_spec: dict | None = None, grabbable_spec: dict | None = None) -> None:
    global replace_basic_armament_feedback_label, replace_advanced_armament_feedback_label, screen_width_ui, screen_height_ui
    if character_spec is None or grabbable_spec is None:
        replace_basic_armament_feedback_label.config(text="")
        replace_basic_armament_feedback_label.place_forget()
        replace_advanced_armament_feedback_label.config(text="")
        replace_advanced_armament_feedback_label.place_forget()
        return

    basic_relx, basic_rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    advanced_rely, _, advanced_relx, _ = get_detection_box_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    basic_relx += REPLACE_ARMAMENT_REL_POS_TO_NAME
    advanced_relx += REPLACE_ARMAMENT_REL_POS_TO_NAME

    update_replace_basic_armament_feedback_label(character_spec, grabbable_spec, basic_relx, basic_rely)
    update_replace_advanced_armament_feedback_label(character_spec, grabbable_spec, advanced_relx, advanced_rely)
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
            character_detection_thread = DetectionThread(detection_id=CHARACTER_DETECTION, function=detect_character, daemon=True)
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
    global enabled, enable_disable_button, character_detection_thread, menu_detection_thread, armament_detection_thread, replace_armament_detection_thread, root
    with enabled_lock:
        enabled = not enabled
        if enabled:
            # Restart threads if they are not alive
            with character_detection_enabled_lock:
                if character_detection_enabled and not character_detection_thread.is_alive():
                    character_detection_thread = DetectionThread(detection_id=CHARACTER_DETECTION, function=detect_character, daemon=True)
                    character_detection_thread.start()
            if not menu_detection_thread.is_alive():
                menu_detection_thread = DetectionThread(detection_id=MENU_DETECTION, function=detect_menu, daemon=True)
                menu_detection_thread.start()
            if not armament_detection_thread.is_alive():
                armament_detection_thread = DetectionThread(detection_id=ARMAMENT_DETECTION_DEFAULT, function=detect_armament, daemon=True)
                armament_detection_thread.start()
            if not replace_armament_detection_thread.is_alive():
                replace_armament_detection_thread = DetectionThread(detection_id=ARMAMENT_DETECTION_DEFAULT_REPLACE, function=detect_armament, daemon=True)
                replace_armament_detection_thread.start()
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
            if replace_armament_detection_thread.is_alive():
                replace_armament_detection_thread.stop()
            # Hide all the Overlay UI elements
            root.withdraw()
        enable_disable_button.config(
            text="Disable" if enabled else "Enable",
            bg=BUTTON_ENABLED_COLOR if enabled else BUTTON_DISABLED_COLOR,
            activebackground=BUTTON_ENABLED_ACTIVE_COLOR if enabled else BUTTON_DISABLED_COLOR,
        )
    save_configs()


def create_control_window() -> Toplevel:
    global enable_disable_button, character_detection_button, advanced_mode_button, screen_height_ui, screen_width_ui, control_window
    SIZE_X = 330
    SIZE_Y = 160
    if len(loaded_extensions) > 0:
        SIZE_Y += 40
    control_window = Toplevel()
    control_window.title(PROGRAM_NAME)
    padding_x = int(screen_width_ui * 0.05)
    padding_y = int(screen_height_ui * 0.15)
    control_window.geometry(f"{SIZE_X}x{SIZE_Y}+{screen_width_ui - SIZE_X - padding_x}+{screen_height_ui - SIZE_Y - padding_y}")
    icon_image = PhotoImage(file=ICON_PATH)
    control_window.iconphoto(True, icon_image)
    control_window.protocol("WM_DELETE_WINDOW", quit_app)

    top_button_frame = Frame(control_window)
    top_button_frame.pack(pady=2, padx=5, fill="x")

    button_style = {
        "font": ("Arial", 12, "bold"),
        "fg": "white",
        "activeforeground": "white",
        "relief": RAISED,
        "bd": 3,
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
    enable_disable_button.pack(side=LEFT, fill="x", expand=True, padx=(0, 2))

    quit_button = Button(top_button_frame, text="Quit", command=quit_app, bg=BUTTON_QUIT_COLOR, activebackground=BUTTON_QUIT_ACTIVE_COLOR, **button_style)
    quit_button.pack(side=LEFT, fill="x", expand=True, padx=(2, 0))

    bottom_button_frame = Frame(control_window)
    bottom_button_frame.pack(pady=2, padx=5, fill="x")

    character_detection_button = Button(
        bottom_button_frame,
        text=f"{'Disable' if character_detection_enabled else 'Enable'} Character Detection",
        command=toggle_character_detection,
        bg=BUTTON_ENABLED_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
        activebackground=BUTTON_ENABLED_ACTIVE_COLOR if character_detection_enabled else BUTTON_DISABLED_COLOR,
        **button_style,
    )
    character_detection_button.pack(side=TOP, fill="x", expand=True, pady=2)

    advanced_mode_button = Button(
        bottom_button_frame,
        text=f"{'Disable' if advanced_mode_enabled else 'Enable'} Advanced Mode",
        command=toggle_advanced_mode,
        bg=BUTTON_ENABLED_COLOR if advanced_mode_enabled else BUTTON_DISABLED_COLOR,
        activebackground=BUTTON_ENABLED_ACTIVE_COLOR if advanced_mode_enabled else BUTTON_DISABLED_ACTIVE_COLOR,
        **button_style,
    )
    advanced_mode_button.pack(side=TOP, fill="x", expand=True, pady=2)
    
    extensions_text = "No extensions loaded."
    if len(loaded_extensions) > 0:
        extensions_text = f"Loaded Extensions (mode: {extension_load_mode}):\n"
        for extension_name, module_names in loaded_extensions.items():
            module_names_py = [f"{module_name}.py" for module_name in module_names]
            extensions_text += f"- {extension_name} ({', '.join(module_names_py)})\n"
    extensions_label = Label(
        control_window,
        text=extensions_text,
        font=("Consolas", 8),
        fg="white",
        bg="black",
        justify="left",
        anchor="nw",
    )
    extensions_label.pack(side=TOP, fill="both", expand=True, padx=5, pady=5)

    version_label = Label(
        control_window,
        text=f"Version {VERSION}",
        font=("Arial", 8),
        fg="gray",
        anchor="sw",
    )
    version_label.place(relx=0.99, rely=1, anchor="se")

    return control_window


# Separate check_confirm_button into two functions to improve readability and maintainability.
def find_button(img: Image.Image) -> bool:
    resolution = f"{img.width}x{img.height}"
    img_np = array(img)
    gray = cvtColor(img_np, COLOR_BGR2GRAY)

    for button_type in BUTTON_TYPES:
        for geometry_type in BUTTON_GEOMETRY_TYPES:
            top, bottom, left, right = get_button_coordinates(img.width, img.height, geometry_type)
            comp_img_np = gray[top:bottom, left:right]
            dimensions = (comp_img_np.shape[1], comp_img_np.shape[0])
            mask_path = path.join(RESOURCES_PATH, "buttons", f"{geometry_type}_mask.png")
            mask_np = array(IMAGE_CACHE.get_image(mask_path))
            mask_np = resize(mask_np, dimensions, interpolation=INTER_AREA)

            for controller_type in CONTROLLER_TYPES_BY_BUTTON_GEOMETRY[geometry_type]:
                ref_img_path = path.join(RESOURCES_PATH, "buttons", f"{button_type}_{controller_type}.png")
                ref_img_np = array(IMAGE_CACHE.get_image(ref_img_path))
                ref_img_np = resize(ref_img_np, dimensions, interpolation=INTER_AREA)

                comp_img_np = bitwise_and(comp_img_np, mask_np)
                ref_img_np = bitwise_and(ref_img_np, mask_np)

                found: bool = not are_images_different(ref_img_np, comp_img_np, 15)
                if found:
                    DEBUG_WINDOW.found_button(button_type, geometry_type, img.width, img.height)
                    return True
    return False


def get_screen_grab() -> Image.Image:
    global last_screengrab, last_screengrab_time, screengrab_lock, screen_width_real, screen_height_real
    with screengrab_lock:
        current_time = time()
        if current_time - last_screengrab_time >= MINIMUM_TIME_BETWEEN_SCREENGRABS or last_screengrab is None:
            last_screengrab = ImageGrab.grab()
            last_screengrab_time = current_time
            if last_screengrab.width != screen_width_real or last_screengrab.height != screen_height_real:
                # Update the real screen dimensions if they have changed
                screen_width_real = last_screengrab.width
                screen_height_real = last_screengrab.height
        return last_screengrab


def get_eff_detection_id(detection_id: str) -> str | None:
    global current_menu_state, current_menu_state_lock
    if detection_id == ARMAMENT_DETECTION_DEFAULT_REPLACE:
        with current_menu_state_lock:
            if current_menu_state == MENU_STATE_DEFAULT:
                return ARMAMENT_DETECTION_DEFAULT_REPLACE
            else:
                return None
    elif detection_id == ARMAMENT_DETECTION_DEFAULT:
        with current_menu_state_lock:
            if current_menu_state == MENU_STATE_DEFAULT:
                return ARMAMENT_DETECTION_DEFAULT
            elif current_menu_state == MENU_STATE_SHOP:
                return ARMAMENT_DETECTION_SHOP
            elif current_menu_state == MENU_STATE_BOSS_DROP:
                return ARMAMENT_DETECTION_BOSS_DROP
    return detection_id


def get_cropped_area(box_identifier: str) -> ndarray | None:
    global button_detection_required
    img = get_screen_grab()
    try:
        button_detected: bool = find_button(img)
        if button_detection_required and not button_detected:
            return None
        elif not button_detection_required and button_detected:
            # The first time that we detect one of the buttons in question, we enable the "detection_required" flag,
            # so that we can start preventing the OCR from running when it's not necessary.
            button_detection_required = True
    except Exception as e:
        log_error(e, fatal=False)
        # Ignore error and continue as normal

    img_np = array(img)
    gray = cvtColor(img_np, COLOR_BGR2GRAY)

    width, height = img.size
    top, bottom, left, right = get_detection_box_coordinates(box_identifier, width, height)
    return gray[top:bottom, left:right]


def detect_text(detection_id: str) -> tuple[int, str]:
    global previous_armament_img, previous_armament_name, last_armament_pixel_set, last_replace_armament_pixel_set, previous_replace_armament_img, previous_replace_armament_name, current_menu_state, current_menu_state_lock, pixelset_cache, screen_width_real, screen_height_real, previous_imgs_lock, previous_matches_lock, last_pixelsets_lock, previous_imgs, previous_matches, last_pixelsets, DEBUG_WINDOW

    # Get a more specific detection ID if necessary, for example, due to the current menu state.
    eff_detection_id = get_eff_detection_id(detection_id)
    if eff_detection_id is None:
        return (TEXT_ORIGIN_NONE, "")

    cropped = get_cropped_area(eff_detection_id)
    if cropped is None:
        return (TEXT_ORIGIN_NONE, "")
    _, img_for_ocr = threshold(cropped, 115, 255, THRESH_BINARY_INV)

    # To avoid unnecessary processing, we check if the image has changed since the last detection.
    with previous_imgs_lock, previous_matches_lock:
        if not are_images_different(previous_imgs[eff_detection_id], cropped):
            return previous_matches[eff_detection_id]

    # To save time and resources in future detection of the same armament, we generate a pixel set
    # and check if it matches any of the previously saved pixel sets.
    pixel_set: PixelSet = PixelSet(pixelset_cache, cropped, screen_width_real, screen_height_real, eff_detection_id)
    pixel_set_match = pixel_set.find_match(eff_detection_id)
    if pixel_set_match != "":
        DEBUG_WINDOW.matched_pixelset(eff_detection_id, pixel_set_match)
        with previous_imgs_lock, previous_matches_lock, last_pixelsets_lock:
            previous_imgs[eff_detection_id] = img_for_ocr
            previous_matches[eff_detection_id] = (TEXT_ORIGIN_PIXELSET, pixel_set_match)
            last_pixelsets[eff_detection_id] = None
        return (TEXT_ORIGIN_PIXELSET, pixel_set_match)

    # If the detection area contains too few relevant colored pixels, we assume that the OCR will be unable to detect anything useful.
    if pixel_set.size() / (pixel_set.width * pixel_set.height) < OCR_MINIMUM_PIXELS_PERCENTS[eff_detection_id]:
        return (TEXT_ORIGIN_NONE, "")

    # Character detection is stable enough that we can ditch the OCR completely if we have already learned a pixel set for each character for this resolution.
    if eff_detection_id == CHARACTER_DETECTION and pixelset_cache.all_characters_learned(screen_width_real, screen_height_real):
        return (TEXT_ORIGIN_NONE, "")

    # Last resource: OCR
    DEBUG_WINDOW.begin_ocr(eff_detection_id, img_for_ocr)
    text = pytesseract.image_to_string(img_for_ocr, config=TESSERACT_CONFIG, lang=TESSERACT_LANG, timeout=TESSERACT_TIMEOUT)
    text = text.strip()
    DEBUG_WINDOW.end_ocr(eff_detection_id, text)

    # Save all the relevant data for the next detection.
    with previous_imgs_lock, previous_matches_lock, last_pixelsets_lock:
        previous_imgs[eff_detection_id] = img_for_ocr
        previous_matches[eff_detection_id] = (TEXT_ORIGIN_OCR, text)
        last_pixelsets[eff_detection_id] = pixel_set
    return (TEXT_ORIGIN_OCR, text)


# -------------------------- Classes ---------------------------#


class DetectionThread(Thread):
    def __init__(self, detection_id: str, function: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()
        self.detection_id = detection_id
        self.function = function

    def run(self) -> None:
        DEBUG_WINDOW.thread_started(self.detection_id)
        while not self.is_stopped():
            t0 = time()
            try:
                self.function(self.detection_id)
            except Exception as e:
                log_error(e)
            t1 = time()
            sleep_time = max(0, DETECTION_LOOP_PERIODS[self.detection_id] - (t1 - t0))
            sleep(sleep_time)
        DEBUG_WINDOW.thread_stopped(self.detection_id)

    def stop(self) -> None:
        self._stop_event.set()

    def is_stopped(self) -> bool:
        return self._stop_event.is_set()


def convert_menu_title_to_state(title: str) -> str:
    if title == SHOP_TITLE:
        return MENU_STATE_SHOP
    elif title == BOSS_DROP_TITLE:
        return MENU_STATE_BOSS_DROP
    return MENU_STATE_DEFAULT


def learn_pixelset(detection_id: str, text_origin: int, match_result: int, match: Any, get_id: Callable) -> None:
    # Learn the pixel set if it is a perfect match
    with last_pixelsets_lock:
        last_pixelset: PixelSet | None = last_pixelsets[detection_id]
        if last_pixelset and text_origin == TEXT_ORIGIN_OCR and match_result == PERFECT_MATCH:
            last_pixelset.write(get_id(match))
        last_pixelsets[detection_id] = None  # Reset the last pixel set


def detect_menu(detection_id: str) -> None:
    global current_menu_state, current_menu_state_lock
    text_origin, text = detect_text(MENU_DETECTION)
    match_result, match = find_match(detection_id, text_origin, text, [BOSS_DROP_TITLE, SHOP_TITLE], convert_menu_title_to_state)
    if match_result == NO_MATCH:
        match = MENU_STATE_DEFAULT
    with current_menu_state_lock:
        if match == current_menu_state:
            return
        DEBUG_WINDOW.found_match(detection_id, text_origin, text, match_result, match)
        current_menu_state = match
        if match != MENU_STATE_DEFAULT:  # Do not learn pixelset for the default menu state (which represents the absence of a menu)
            learn_pixelset(detection_id, text_origin, match_result, match, lambda x: x)


def detect_character(detection_id: str) -> None:
    global current_character_name, current_character_name_lock, character_detection_enabled, character_detection_enabled_lock, DEBUG_WINDOW
    with character_detection_enabled_lock:
        if not character_detection_enabled:
            return
    text_origin, text = detect_text(detection_id)
    match_result, match = find_match(detection_id, text_origin, text, CHARACTER_SPECS, lambda character_spec: character_spec["name"])
    if match_result == NO_MATCH:
        return
    with current_character_name_lock:
        if match["name"] != current_character_name:
            DEBUG_WINDOW.found_match(detection_id, text_origin, text, match_result, match["name"])
            current_character_name = match["name"]
            update_current_character_dropdown(match["name"])
            learn_pixelset(detection_id, text_origin, match_result, match, lambda x: x["name"])


def detect_armament(detection_id: str) -> None:
    character_spec: dict | None = get_current_character_spec()
    if character_spec is None:
        return
    text_origin, text = detect_text(detection_id)
    match_result, match_spec = find_match(detection_id, text_origin, text, GRABBABLE_SPECS, lambda grabbable_spec: grabbable_spec["name"])
    if match_result == NO_MATCH:
        update_armament_feedback_labels_general(detection_id)
        return
    DEBUG_WINDOW.found_match(detection_id, text_origin, text, match_result, match_spec["name"])
    update_armament_feedback_labels_general(detection_id, character_spec, match_spec)
    eff_detection_id = get_eff_detection_id(detection_id)
    if eff_detection_id is not None:
        learn_pixelset(eff_detection_id, text_origin, match_result, match_spec, lambda x: x["id"])


# -------------------------- Main ------------------------------#


if __name__ == "__main__":
    load_configs()
    makedirs(PROGRAM_DATA_PATH, exist_ok=True)
    makedirs(PIXEL_SETS_PATH, exist_ok=True)
    makedirs(EXTENSIONS_PATH, exist_ok=True)
    if DEBUG:
        makedirs(DEBUG_PATH, exist_ok=True)

    root = Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "black")
    icon_image = PhotoImage(file=ICON_PATH)
    root.iconphoto(True, icon_image)

    screen_width_ui = root.winfo_screenwidth()
    screen_height_ui = root.winfo_screenheight()

    img = ImageGrab.grab()
    screen_width_real = img.width
    screen_height_real = img.height
    del img

    root.geometry(f"{screen_width_ui}x{screen_height_ui}+0+0")
    root.config(bg="black")
    root.withdraw()

    basic_armament_feedback_label_font_size = int(screen_height_ui * 0.014)
    advanced_armament_feedback_label_font_size = int(screen_height_ui * 0.012)
    current_character_label_font_size = int(screen_height_ui * 0.008)

    basic_armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Arial", basic_armament_feedback_label_font_size))
    basic_armament_feedback_label.pack()
    relx, rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    basic_armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")

    advanced_armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Consolas", advanced_armament_feedback_label_font_size))
    advanced_armament_feedback_label.pack()
    rely, _, relx, _ = get_detection_box_coordinates(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    advanced_armament_feedback_label.place(relx=relx, rely=rely, anchor="sw")

    replace_basic_armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Arial", basic_armament_feedback_label_font_size))
    replace_basic_armament_feedback_label.pack()
    relx, rely = get_ui_element_coordinates_rel(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    relx += REPLACE_ARMAMENT_REL_POS_TO_NAME
    replace_basic_armament_feedback_label.place(relx=relx, rely=rely, anchor="nw")

    replace_advanced_armament_feedback_label = Label(root, text="", fg="white", bg="black", font=("Consolas", advanced_armament_feedback_label_font_size))
    replace_advanced_armament_feedback_label.pack()
    rely, _, relx, _ = get_detection_box_coordinates(ARMAMENT_DETECTION_DEFAULT, screen_width_ui, screen_height_ui)
    relx += REPLACE_ARMAMENT_REL_POS_TO_NAME
    replace_advanced_armament_feedback_label.place(relx=relx, rely=rely, anchor="sw")

    current_character_var = StringVar(value=NO_CHARACTER)

    current_character_dropdown = OptionMenu(root, current_character_var, *CHARACTERS, command=on_character_selected)
    current_character_dropdown.config(bg="black", fg="white", font=("Arial", current_character_label_font_size), bd=0, highlightthickness=0)
    current_character_dropdown["menu"].config(bg="black", fg="white", font=("Arial", current_character_label_font_size))
    relx, rely = get_ui_element_coordinates_rel("character_dropdown", screen_width_ui, screen_height_ui)
    current_character_dropdown.place(relx=relx, rely=rely, anchor="ne")

    character_detection_thread = DetectionThread(detection_id=CHARACTER_DETECTION, function=detect_character, daemon=True)
    menu_detection_thread = DetectionThread(detection_id=MENU_DETECTION, function=detect_menu, daemon=True)
    armament_detection_thread = DetectionThread(detection_id=ARMAMENT_DETECTION_DEFAULT, function=detect_armament, daemon=True)
    replace_armament_detection_thread = DetectionThread(detection_id=ARMAMENT_DETECTION_DEFAULT_REPLACE, function=detect_armament, daemon=True)
    DEBUG_WINDOW = DebugWindow(root, DEBUG, DEBUG_PATH)

    extensible_function_specs = {
        "get_basic_label_icons" : getfullargspec(get_basic_label_icons),
        "get_advanced_label_text" : getfullargspec(get_advanced_label_text)
    }
    extension_load_mode, loaded_extensions = load_extensions(EXTENSIONS_PATH, extensible_function_specs)
    load_all_character_specs(RESOURCES_PATH)
    load_all_grabbable_specs(RESOURCES_PATH)
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
        replace_armament_detection_thread.start()
        print("Ready!")
        root.mainloop()
    except Exception as e:
        log_error(e, True)
    except KeyboardInterrupt:
        print("Manual program stop.")
        quit_app()
