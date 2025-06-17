from tkinter import Tk, Toplevel, Canvas
from lib.constants import *


class DebugWindow:
    def __init__(self, root: Tk):
        self.debug_window = Toplevel(root)
        self.screen_width = self.debug_window.winfo_screenwidth()
        self.screen_height = self.debug_window.winfo_screenheight()
        self.debug_window.overrideredirect(True)
        self.debug_window.attributes("-topmost", True)
        self.debug_window.wm_attributes("-transparentcolor", "black")
        self.debug_window.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.debug_canvas = Canvas(self.debug_window, width=self.screen_width, height=self.screen_height, bg="black", highlightthickness=0)
        self.debug_canvas.pack()

        self.menu_title_rect = None
        self.character_rect = None
        self.armament_rect = None

    def show_armament_rect(self, box_identifier: str) -> None:
        if self.armament_rect:
            self.debug_canvas.delete(self.armament_rect)
        top, bottom, left, right = get_detection_box(box_identifier, self.screen_width, self.screen_height)
        self.armament_rect = self.debug_canvas.create_rectangle(left, top, right, bottom, outline="red", width=2)

    def hide_armament_rect(self) -> None:
        if self.armament_rect:
            self.debug_canvas.delete(self.armament_rect)
            self.armament_rect = None

    def show_menu_title_rect(self) -> None:
        if self.menu_title_rect:
            self.debug_canvas.delete(self.menu_title_rect)
        top, bottom, left, right = get_detection_box("menu_title", self.screen_width, self.screen_height)
        self.menu_title_rect = self.debug_canvas.create_rectangle(left, top, right, bottom, outline="yellow", width=2)

    def hide_menu_title_rect(self) -> None:
        if self.menu_title_rect:
            self.debug_canvas.delete(self.menu_title_rect)
            self.menu_title_rect = None

    def show_character_rect(self) -> None:
        if self.character_rect:
            self.debug_canvas.delete(self.character_rect)
        top, bottom, left, right = get_detection_box("character", self.screen_width, self.screen_height)
        self.character_rect = self.debug_canvas.create_rectangle(left, top, right, bottom, outline="blue", width=2)

    def hide_character_rect(self) -> None:
        if self.character_rect:
            self.debug_canvas.delete(self.character_rect)
            self.character_rect = None
