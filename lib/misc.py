from imagehash import average_hash, ImageHash
from textdistance import jaccard
from numpy import ndarray
from PIL import Image
from os import path, makedirs, listdir
from cv2 import threshold, THRESH_BINARY
from lib.constants import *
from lib.armaments import *
from re import sub
from typing import Iterable, Any, Callable


def text_matches(rough_text: str, target_text: str, detection_id: str) -> tuple[int, float]:
    threshold: float = TEXT_SIMILARITY_THRESHOLDS[detection_id]
    clean_target_text: str = target_text.strip().upper()
    clean_target_text = clean_target_text.replace("É", "E").replace("é", "E")
    clean_target_text = sub(r"[^a-zA-Z\s\'\-\.]", "", clean_target_text)  # Will mainly remove: []0-9

    clean_rough_text: str = rough_text.strip().upper()
    clean_rough_text = clean_rough_text.replace("’", "'").replace("‘", "'")
    clean_rough_text = clean_rough_text.replace("!", "L").replace("+", "T")
    clean_rough_text = clean_rough_text.replace("É", "E").replace("é", "E")
    clean_rough_text = sub(r"[^a-zA-Z\s\'\-\.]", "", clean_rough_text)
    clean_rough_text = sub(r"\s+", " ", clean_rough_text)

    similarity = jaccard.normalized_similarity(clean_rough_text, clean_target_text)
    if similarity >= threshold:
        if clean_rough_text == clean_target_text:
            return (PERFECT_MATCH, 1)
        return (GOOD_MATCH, similarity)
    return (NO_MATCH, 0)


def find_match(detection_id: str, text_origin: int, text: str, search_space: Iterable, get_text: Callable, exhaustive: bool = True) -> tuple[int, Any]:
    if text_origin == TEXT_ORIGIN_NONE or text == "":
        return (NO_MATCH, None)
    if text_origin == TEXT_ORIGIN_PIXELSET:
        for item in search_space:
            item_text: str = get_text(item)
            if text == item_text:
                return (PERFECT_MATCH, item)
    if text_origin == TEXT_ORIGIN_OCR:
        best_match: Any = None
        best_match_similarity: float = 0.0
        for item in search_space:
            item_text: str = get_text(item)
            match_result, similarity = text_matches(text, item_text, detection_id)
            if match_result == PERFECT_MATCH:
                return (PERFECT_MATCH, item)
            elif match_result == GOOD_MATCH:
                if exhaustive:
                    if similarity > best_match_similarity:
                        best_match = item
                        best_match_similarity = similarity
                        print(f"Found good match: {item_text} (similarity: {similarity})")
                else:
                    return (match_result, item)
    if exhaustive and best_match is not None:
        return (GOOD_MATCH, best_match)
    return (NO_MATCH, None)


def are_images_different(previous_img: ndarray | None, current_img: ndarray, cutoff: int = 1) -> bool:
    if previous_img is None:
        return True  # If no previous image, consider it a change

    pil_current_img: Image.Image = Image.fromarray(current_img)
    pil_previous_img: Image.Image = Image.fromarray(previous_img)

    hash0: ImageHash = average_hash(pil_current_img)
    hash1: ImageHash = average_hash(pil_previous_img)

    hashDiff = hash0 - hash1  # Finds the distance between the hashes of images
    if cutoff == 11:
        print(f"Hash difference: {hashDiff}")
    return hashDiff >= cutoff


class ImageCache:
    def __init__(self):
        self.cache: dict[str, Image.Image] = {}

    def get_image(self, image_path: str) -> Image.Image:
        if image_path not in self.cache:
            if not path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            with open(image_path, mode="rb") as file:
                self.cache[image_path] = Image.open(file).convert("L")
        return self.cache[image_path]


class PixelSetCache:
    def __init__(self, base_path: str, debug: bool = False):
        self.base_path: str = base_path
        self.debug: bool = debug
        self.cache: dict[str, dict[str, dict[str, set[tuple[int, int]]]]] = {}
        if not path.exists(base_path):
            return
        if self.debug:
            print("Loading pixel sets to cache...")
        for resolution in listdir(base_path):
            resolution_path = path.join(base_path, resolution)
            if not path.isdir(resolution_path):
                continue
            for detection_box_id in listdir(resolution_path):
                detection_box_path = path.join(resolution_path, detection_box_id)
                if not path.isdir(detection_box_path):
                    continue
                for filename in listdir(detection_box_path):
                    pixelset_path = path.join(detection_box_path, filename)
                    if not path.isfile(pixelset_path) or not filename.endswith(".pixelset"):
                        continue
                    identifier = path.splitext(filename)[0]
                    if self.get_pixelset(resolution, detection_box_id, identifier) is None:
                        pixelset = self.read_pixelset(pixelset_path)
                        self.set_pixelset(resolution, detection_box_id, identifier, pixelset)
                        if self.debug:
                            print(f"Loaded pixel set: {resolution}/{detection_box_id}/{identifier}.pixelset")
        if self.debug:
            print("Finished loading pixel sets to cache.")

    def get_pixelset(self, resolution: str, detection_box_id: str, identifier: str) -> set[tuple[int, int]] | None:
        if resolution in self.cache and detection_box_id in self.cache[resolution] and identifier in self.cache[resolution][detection_box_id]:
            return self.cache[resolution][detection_box_id][identifier]
        return None

    def get_pixelsets(self, resolution: str, detection_box_id: str) -> dict[str, set[tuple[int, int]]]:
        if resolution in self.cache and detection_box_id in self.cache[resolution]:
            return self.cache[resolution][detection_box_id]
        return {}

    def set_pixelset(self, resolution: str, detection_box_id: str, identifier: str, pixelset: set[tuple[int, int]]) -> None:
        if resolution not in self.cache:
            self.cache[resolution] = {}
        if detection_box_id not in self.cache[resolution]:
            self.cache[resolution][detection_box_id] = {}
        if not pixelset or len(pixelset) < 10:
            return
        self.cache[resolution][detection_box_id][identifier] = pixelset

    def save_pixelset(self, resolution: str, detection_box_id: str, identifier: str, pixelset: set[tuple[int, int]]) -> None:
        if resolution not in self.cache:
            self.cache[resolution] = {}
        if detection_box_id not in self.cache[resolution]:
            self.cache[resolution][detection_box_id] = {}
        self.cache[resolution][detection_box_id][identifier] = pixelset

        # Write-through to disk
        tgt_path = path.join(self.base_path, resolution, detection_box_id)
        makedirs(tgt_path, exist_ok=True)
        pixelset_path = path.join(tgt_path, f"{identifier}.pixelset")
        with open(pixelset_path, "w") as file:
            for x, y in pixelset:
                file.write(f"{x} {y}\n")

    def read_pixelset(self, filepath: str) -> set[tuple[int, int]]:
        if not path.exists(filepath):
            return set()
        with open(filepath, "r") as file:
            lines = file.readlines()
        pixelset: set[tuple[int, int]] = set()
        for line in lines:
            line = line.strip()
            if line:
                x, y = map(int, line.split())
                pixelset.add((x, y))
        return pixelset

    def clear_cache(self) -> None:
        self.cache = {}

    def all_characters_learned(self, screen_width: int, screen_height: int) -> bool:
        resolution = f"{screen_width}x{screen_height}"
        detection_box_id = MENU_DETECTION
        pixelset_characters: list[str] = list(self.get_pixelsets(resolution, detection_box_id).keys())
        return all(character in pixelset_characters for character in CHARACTERS)


class PixelSet:
    def __init__(
        self,
        cache: PixelSetCache,
        cropped: ndarray,
        screen_width: int,
        screen_height: int,
        detection_id: str,
    ):
        self.cache: PixelSetCache = cache
        self.cropped: ndarray = cropped
        self.resolution: str = f"{screen_width}x{screen_height}"
        self.detection_id: str = detection_id
        self.fn_rate: float = PIXELSET_FN_RATES[detection_id]
        self.fp_rate: float = PIXELSET_FP_RATES[detection_id]
        self.pixelset_threshold: int = PIXELSET_THRESHOLDS[detection_id]
        threshold_reduction: int = PIXELSET_THRESHOLD_REDUCTIONS[detection_id]
        self.pixelset: set = set()
        _, self.image = threshold(cropped, self.pixelset_threshold - threshold_reduction, 255, THRESH_BINARY)
        self.height, self.width = cropped.shape[:2]
        for y in range(self.height):
            for x in range(self.width):
                if self.image[y, x] == 255:
                    self.pixelset.add((x, y))

    def size(self) -> int:
        return len(self.pixelset)

    def write(self, identifier: str) -> None:
        _, ref_image = threshold(self.cropped, self.pixelset_threshold, 255, THRESH_BINARY)
        ref_pixelset: set = set()
        for y in range(self.height):
            for x in range(self.width):
                if ref_image[y, x] == 255:
                    ref_pixelset.add((x, y))
        if len(ref_pixelset) < 10:
            return  # Require at least 10 pixels to write
        self.cache.save_pixelset(self.resolution, self.detection_id, identifier, ref_pixelset)

    def find_match(self, detection_id: str, exhaustive: bool = True) -> str:
        if len(self.pixelset) < 10:
            return ""
        pixelsets: dict[str, set[tuple[int, int]]] = self.cache.get_pixelsets(self.resolution, self.detection_id)
        best_match: str = ""
        best_fn_rate: float = 1.0
        for identifier in pixelsets.keys():
            ref_pixelset: set = pixelsets[identifier]
            fn_rate = len(ref_pixelset - self.pixelset) / len(ref_pixelset) if ref_pixelset else 0
            fp_rate = len(self.pixelset - ref_pixelset) / len(self.pixelset) if self.pixelset else 0
            if fn_rate <= self.fn_rate and fp_rate <= self.fp_rate:
                if exhaustive:
                    if best_match == "" or (fn_rate < best_fn_rate):
                        if detection_id in ARMAMENT_DETECTION_IDS:
                            try:
                                match = find_grabbable_name_by_id(identifier)
                            except:
                                match = ""
                        else:
                            match = identifier
                        best_match = match
                        best_fn_rate = fn_rate
                else:
                    if detection_id in ARMAMENT_DETECTION_IDS:
                        try:
                            match = find_grabbable_name_by_id(identifier)
                        except:
                            match = ""
                    else:
                        match = identifier
                    return match
        if exhaustive:
            return best_match
        return ""  # No match found


def version_is_older(version: str, target_version: str) -> bool:
    numbers = list(map(int, version.split(".")))
    target_numbers = list(map(int, target_version.split(".")))

    for num, t_num in zip(numbers, target_numbers):
        if num < t_num:
            return True
        elif num > t_num:
            return False
    # Identical versions
    return False


def get_button_coordinates(width: int, height: int, control_type: str) -> tuple[int, int, int, int]:
    # Check if the screen resolution is more wide than 16:9 or more tall than 16:9
    if (width / height) > (16 / 9):  # Wider than 16:9
        # Find width occupied by black bars
        black_bars_height = 0
        black_bars_width = width - (height * 16 / 9)
    elif (width / height) < (16 / 9):  # Taller than 16:9
        # Find height occupied by black bars
        black_bars_height = height - (width * 9 / 16)
        black_bars_width = 0
    else:  # Exactly 16:9
        black_bars_height = 0
        black_bars_width = 0

    if black_bars_height == 0 and black_bars_width == 0:
        return BUTTON_COORDINATES[f"{width}x{height}"][control_type]
    elif black_bars_height == 0:  # Wider than 16:9
        for res in BUTTON_COORDINATES:
            w, h = map(int, res.split("x"))
            if height == h:
                coordinates = BUTTON_COORDINATES[res][control_type]
                return (coordinates[0] + int(black_bars_width / 2), coordinates[1] + int(black_bars_width / 2), coordinates[2], coordinates[3])
    elif black_bars_width == 0:  # Taller than 16:9
        for res in BUTTON_COORDINATES:
            w, h = map(int, res.split("x"))
            if width == w:
                coordinates = BUTTON_COORDINATES[res][control_type]
                return (coordinates[0], coordinates[1], coordinates[2] + int(black_bars_height / 2), coordinates[3] + int(black_bars_height / 2))
    coordinates_4k = BUTTON_COORDINATES["3840x2160"][control_type]
    coordinates_rel = (coordinates_4k[0] / 2160, coordinates_4k[1] / 2160, coordinates_4k[2] / 3840, coordinates_4k[3] / 3840)
    return (
        int(((height - black_bars_height) * coordinates_rel[0]) + black_bars_height / 2),
        int(((height - black_bars_height) * coordinates_rel[1]) + black_bars_height / 2),
        int(((width - black_bars_width) * coordinates_rel[2]) + black_bars_width / 2),
        int(((width - black_bars_width) * coordinates_rel[3]) + black_bars_width / 2),
    )


def get_detection_box_coordinates(identifier: str, screen_width: int, screen_height: int) -> tuple[int, int, int, int]:
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


def get_detection_box_coordinates_rel(identifier: str, screen_width: int, screen_height: int) -> tuple[float, float, float, float]:
    top, bottom, left, right = get_detection_box_coordinates(identifier, screen_width, screen_height)
    return top / screen_height, bottom / screen_height, left / screen_width, right / screen_width


def get_ui_element_coordinates_rel(identifier: str, screen_width: int, screen_height: int) -> tuple[float, float]:
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
