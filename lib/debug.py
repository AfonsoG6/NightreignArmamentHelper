from tkinter import Tk, Toplevel, Canvas
from numpy import ndarray
from cv2 import imwrite
from os import path, makedirs
from datetime import datetime
from lib.constants import *


class DebugWindow:
    def __init__(self, root: Tk, debug: bool, debug_path: str) -> None:
        self.debug = debug
        self.debug_path = debug_path
        if not debug:
            return
        self.debug_window = Toplevel(root)
        self.screen_width = self.debug_window.winfo_screenwidth()
        self.screen_height = self.debug_window.winfo_screenheight()
        self.debug_window.overrideredirect(True)
        self.debug_window.attributes("-topmost", True)
        self.debug_window.wm_attributes("-transparentcolor", "black")
        self.debug_window.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.debug_canvas = Canvas(self.debug_window, width=self.screen_width, height=self.screen_height, bg="black", highlightthickness=0)
        self.debug_canvas.pack()

        self.rectangles = {}
        self.colors = {
            ARMAMENT_DETECTION_DEFAULT: "green",
            ARMAMENT_DETECTION_DEFAULT_REPLACE: "cyan",
            ARMAMENT_DETECTION_BOSS_DROP: "green",
            ARMAMENT_DETECTION_SHOP: "green",
            MENU_DETECTION: "yellow",
            CHARACTER_DETECTION: "blue",
        }

    def show_rectangle(self, detection_id: str) -> None:
        if not self.debug:
            return
        if detection_id in self.rectangles and self.rectangles[detection_id]:
            self.debug_canvas.delete(self.rectangles[detection_id])
        top, bottom, left, right = get_detection_box(detection_id, self.screen_width, self.screen_height)
        self.rectangles[detection_id] = self.debug_canvas.create_rectangle(left, top, right, bottom, outline=self.colors[detection_id], width=2)

    def hide_rectangle(self, detection_id: str) -> None:
        if not self.debug:
            return
        if detection_id in self.rectangles and self.rectangles[detection_id]:
            self.debug_canvas.delete(self.rectangles[detection_id])
            self.rectangles[detection_id] = None

    def matched_pixelset(self, detection_id: str, text: str) -> None:
        if not self.debug:
            return
        print(f"Debug: Matched pixel set for {detection_id} with text: '{text}'")

    def begin_ocr(self, detection_id: str, img_for_ocr: ndarray) -> None:
        if not self.debug:
            return
        self.show_rectangle(detection_id)
        makedirs(self.debug_path, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = path.join(self.debug_path, f"{detection_id}_{timestamp}.png")
        imwrite(filename, img_for_ocr)

    def end_ocr(self, detection_id: str, raw_text: str) -> None:
        if not self.debug:
            return
        self.hide_rectangle(detection_id)
        print(f"Debug: OCR completed for {detection_id}, obtained the raw text: {raw_text}")

    def found_match(self, detection_id: str, text_origin: int, text: str, match_result: int, match: str) -> None:
        if not self.debug:
            return
        text_origin_text = ""
        if text_origin == TEXT_ORIGIN_NONE:
            text_origin_text = "NONE"
        elif text_origin == TEXT_ORIGIN_OCR:
            text_origin_text = "OCR"
        elif text_origin == TEXT_ORIGIN_PIXELSET:
            text_origin_text = "PIXELSET"
        match_result_text = ""
        if match_result == NO_MATCH:
            match_result_text = "NO_MATCH"
        elif match_result == GOOD_MATCH:
            match_result_text = "GOOD_MATCH"
        elif match_result == PERFECT_MATCH:
            match_result_text = "PERFECT_MATCH"
        print(f"Debug: Found match for {detection_id}. Text origin: {text_origin_text}, Text: '{text}' - Match result: {match_result_text}, Match: '{match}'")

    def thread_started(self, thread_name: str) -> None:
        if not self.debug:
            return
        print(f"Debug: Thread '{thread_name}' has started.")

    def thread_stopped(self, thread_name: str) -> None:
        if not self.debug:
            return
        print(f"Debug: Thread '{thread_name}' has stopped.")
