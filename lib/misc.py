from imagehash import average_hash, ImageHash
from textdistance import jaccard
from numpy import ndarray
from PIL import Image
from os import path, makedirs, listdir
from cv2 import threshold, THRESH_BINARY, imwrite
from lib.constants import *
from re import sub

TEXT_MATCH_RESULTS: list[int] = [
    FALSE := 0,
    TRUE := 1,
    PERFECT := 2,
]


def text_matches(rough_text: str, target_text: str, threshold: float = TEXT_DISTANCE_THRESHOLD) -> int:
    """
    Check if the rough text matches the target text based on a Jaccard similarity threshold.
    """
    clean_target_text: str = target_text.strip().upper()
    clean_rough_text: str = rough_text.strip().upper()
    clean_rough_text = clean_rough_text.replace("’", "'").replace("‘", "'")
    clean_rough_text = clean_rough_text.replace("!", "l").replace("+", "t")
    clean_rough_text = sub(r"[^a-zA-ZéÉ\'\-\.]", "", clean_rough_text)
    clean_rough_text = sub(r"\s+", " ", clean_rough_text)

    if jaccard.normalized_similarity(clean_rough_text, clean_target_text) >= threshold:
        if clean_rough_text == clean_target_text:
            return PERFECT
        return TRUE
    return FALSE


def image_changed(previous_img: ndarray | None, current_img: ndarray) -> bool:
    if previous_img is None:
        return True  # If no previous image, consider it a change

    pil_current_img: Image.Image = Image.fromarray(current_img)
    pil_previous_img: Image.Image = Image.fromarray(previous_img)

    hash0: ImageHash = average_hash(pil_current_img)
    hash1: ImageHash = average_hash(pil_previous_img)

    cutoff = 1
    hashDiff = hash0 - hash1  # Finds the distance between the hashes of images
    return hashDiff >= cutoff


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
        """
        Check if all characters have learned pixel sets for the given screen resolution.
        :param screen_width: Width of the screen.
        :param screen_height: Height of the screen.
        :return: True if all characters have learned pixel sets, False otherwise.
        """
        resolution = f"{screen_width}x{screen_height}"
        detection_box_id = "character"
        pixelset_characters: list[str] = list(self.get_pixelsets(resolution, detection_box_id).keys())
        return all(
            character in pixelset_characters for character in CHARACTERS
        )


class PixelSet:
    def __init__(
        self,
        cache: PixelSetCache,
        cropped: ndarray,
        screen_width: int,
        screen_height: int,
        detection_box_id: str,
        pixelset_threshold: int,
        threshold_reduction: int,
        fn_rate: float,
        fp_rate: float,
    ):
        self.cache: PixelSetCache = cache
        self.cropped: ndarray = cropped
        self.resolution: str = f"{screen_width}x{screen_height}"
        self.detection_box_id: str = detection_box_id
        self.fn_rate: float = fn_rate
        self.fp_rate: float = fp_rate
        self.pixelset_threshold: int = pixelset_threshold
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
        self.cache.save_pixelset(self.resolution, self.detection_box_id, identifier, ref_pixelset)

    def find_match(self) -> str:
        if len(self.pixelset) < 10:
            return ""
        pixelsets: dict[str, set[tuple[int, int]]] = self.cache.get_pixelsets(self.resolution, self.detection_box_id)
        for identifier in pixelsets.keys():
            ref_pixelset: set = pixelsets[identifier]
            fn_rate = len(ref_pixelset - self.pixelset) / len(ref_pixelset) if ref_pixelset else 0
            fp_rate = len(self.pixelset - ref_pixelset) / len(self.pixelset) if self.pixelset else 0
            if fn_rate <= self.fn_rate and fp_rate <= self.fp_rate:
                return identifier
        return ""  # No match found
