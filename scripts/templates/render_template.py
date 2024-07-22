import json
import os
import random

from PIL import ImageDraw, ImageFont

from scripts.generators import text_generators
from scripts.templates.common import generate_card_image
from scripts.color.conversion import rgb_to_hex
from scripts.color.generate_pallet import generate_random_palette
from scripts.color.text_color import best_text_color_from_palette


def get_random_template_content(root_path, side="front"):
    templates_dir = os.path.join(root_path, 'assets', 'templates', side)
    counter_file_path = os.path.join(templates_dir, 'counter.txt')

    if not os.path.exists(counter_file_path):
        raise FileNotFoundError(f"Counter file not found at '{counter_file_path}'")

    # Read the counter file to determine the number of templates
    with open(counter_file_path, 'r') as counter_file:
        template_count = int(counter_file.read().strip())

    if template_count <= 0:
        raise ValueError("No templates available")

    # Choose a random template number
    random_template_number = random.randint(1, template_count)
    random_template_name = f'template_{random_template_number}'
    random_template_path = os.path.join(templates_dir, f'{random_template_name}.json')

    if not os.path.exists(random_template_path):
        raise FileNotFoundError(f"Template '{random_template_name}' not found in '{random_template_path}'")

    # Read the content of the random template
    with open(random_template_path, 'r') as template_file:
        template_content = json.load(template_file)

    return template_content


def draw_left_justified_text(draw, image_size, position, text, font, color=(0, 0, 0), draw_rectangle=False):
    width, height = image_size

    draw.text(position, text, font=font, fill=color)
    bbox = draw.textbbox(position, text, font=font)

    x0, y0, x1, y1 = bbox

    if draw_rectangle:
        draw.rectangle([(x0, y0), (x1, y1)])

    x0_rel = x0 / width
    y0_rel = y0 / height
    x1_rel = x1 / width
    y1_rel = y1 / height

    return x0_rel, y0_rel, x1_rel, y1_rel


def draw_right_justified_text(draw, image_size, position, text, font, color=(0, 0, 0), draw_rectangle=False):
    image_width, image_height = image_size

    lines = text.split('\n')
    line_widths = [draw.textlength(line, font=font) for line in lines]

    x0, y0 = float('inf'), float('inf')
    x1, y1 = float('-inf'), float('-inf')

    # Draw each line of text right justified
    for i, line in enumerate(lines):
        line_width = line_widths[i]
        x = position[0] - line_width
        y = position[1] + i * font.size

        # Update the bounding box
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, position[0])
        y1 = max(y1, y + font.size)

        draw.text((x, y), line, font=font, fill=color)

    if draw_rectangle:
        draw.rectangle([(x0, y0), (x1, y1)])

    # Normalize the bounding box coordinates
    x0_rel = x0 / image_width
    y0_rel = y0 / image_height
    x1_rel = x1 / image_width
    y1_rel = y1 / image_height

    return x0_rel, y0_rel, x1_rel, y1_rel


def write_fields(template, image, text_color, fonts_path):
    draw = ImageDraw.Draw(image)

    elements_bound_boxes = []

    for element in template['elements']:
        element_type = element['type']
        text_generator = text_generators.get(element_type, None)
        text = text_generator() if text_generator is not None else element['text']

        x0, y0 = element['coordinates'][:2]
        text_height_in_percentage = element['height']
        justified = element.get('justified', 'left')

        # Calculate font size based on the element height
        image_width, image_height = image.size
        font_size = int(text_height_in_percentage * image_height) / 2

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        position = x0 * image_width, y0 * image_height

        if justified == 'right':
            relative_bounding_box = draw_right_justified_text(draw, image.size, position, text, font, text_color)
        else:
            relative_bounding_box = draw_left_justified_text(draw, image.size, position, text, font, text_color)

        elements_bound_boxes.append({
            "type": element_type,
            "relativeBoundingBox": relative_bounding_box
        })

    return elements_bound_boxes


def render_template(width=900, height=540, root_path="..", side="front", fonts_path=None):
    fonts_path = os.path.join(root_path, "assets/fonts") if fonts_path is None else fonts_path

    template = get_random_template_content(root_path, side=side)

    palette = generate_random_palette()
    background_color = palette['Primary']

    text_color = best_text_color_from_palette(palette, background_color)
    text_color_hex = rgb_to_hex(text_color)

    card_image = generate_card_image(background_color, width, height)

    relative_bounding_boxes = write_fields(
        template,
        card_image,
        text_color_hex,
        fonts_path
    )

    return card_image, relative_bounding_boxes
