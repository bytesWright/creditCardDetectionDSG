import os

from PIL import ImageFont

from scripts.generators.generate_random_background import generate_random_background
from scripts.templates.get_all_font_files_by_thickness import get_random_font_path_by_thickness


def ensure_output_directory(output_path):
    if output_path is not None:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)


def generate_card_image(background_color, width=300, height=180):
    image = generate_random_background(width, height, background_color)
    return image


def get_font(fonts_path, font_size):
    if fonts_path is None:
        return ImageFont.load_default()
    else:
        try:
            font_path = get_random_font_path_by_thickness(fonts_path, "Bold")
            return ImageFont.truetype(font_path, font_size)
        except IOError:
            return ImageFont.load_default()


def draw_text_and_get_bbox(draw, position, text, font, fill):
    draw.text(position, text, fill=fill, font=font)
    return draw.textbbox(position, text, font=font)
