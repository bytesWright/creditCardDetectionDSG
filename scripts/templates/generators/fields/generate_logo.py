import os
import os.path
import random

from scripts.templates.convert_svg_to_png import svg_to_pil_image




def get_random_payment_network_logo(root_path=None, current_path=None, image=None, width=None, height=None):
    if current_path is None:
        current_path = os.path.join(root_path, "assets", "images", "logo_card_type")
        current_path = os.path.abspath(current_path)

    # List all SVG files in the directory
    options = [f for f in os.listdir(current_path)]

    # Pick a random SVG file
    option = random.choice(options)
    candidate_path = current_path = os.path.join(current_path, option)

    if os.path.isdir(candidate_path):
        return get_random_payment_network_logo(current_path=candidate_path, image=image, width=width, height=height)

    # Convert SVG to PIL RGBA image
    w, h = image.size

    width = width * w if width is not None else None
    height = height * h if height is not None else None
    return svg_to_pil_image(candidate_path, width, height)
