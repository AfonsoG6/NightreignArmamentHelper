from imagehash import average_hash, ImageHash
from textdistance import jaccard
from numpy import ndarray
from PIL import Image
from lib.constants import ARMAMENT_TEXT_DISTANCE_THRESHOLD

def text_matches(rough_text: str, target_text: str, threshold: float = ARMAMENT_TEXT_DISTANCE_THRESHOLD) -> bool:
    """
    Check if the rough text matches the target text based on a Jaccard similarity threshold.
    """
    clean_target_text: str = target_text.strip().upper()
    
    clean_rough_text: str = rough_text.strip().upper()
    clean_rough_text = clean_rough_text[: min(len(clean_rough_text), len(clean_target_text))]
    
    return jaccard.normalized_similarity(clean_rough_text, clean_target_text) >= threshold

def image_changed(previous_img: ndarray|None, current_img: ndarray) -> bool:
    if previous_img is None:
        return True  # If no previous image, consider it a change

    pil_current_img: Image.Image = Image.fromarray(current_img)
    pil_previous_img: Image.Image = Image.fromarray(previous_img)

    hash0: ImageHash = average_hash(pil_current_img)
    hash1: ImageHash = average_hash(pil_previous_img)
    
    cutoff = 1
    hashDiff = hash0 - hash1  # Finds the distance between the hashes of images
    return hashDiff >= cutoff