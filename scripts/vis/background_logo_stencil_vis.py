import random
import xml.etree.ElementTree as ET
from io import BytesIO

import cairosvg
from PIL import Image

from scripts.color.generate_pallet import generate_random_palette
from scripts.generators import generate_random_background


def compute_stencil_scale_factor(size_a, size_b):
    """
    Compute the scale factor to fit size_b within size_a while maintaining proportions.

    Parameters:
    size_a (tuple): Target size (width, height).
    size_b (tuple): Original size (width, height).

    Returns:
    float: Scale factor.
    """
    width_a, height_a = size_a
    width_b, height_b = size_b

    # Calculate the scaling factors for width and height
    scale_width = width_a / width_b
    scale_height = height_a / height_b

    return min(scale_width, scale_height)


def convert_svg_to_png(svg_path, canvas_width, canvas_height):
    """
    Convert an SVG file to a PNG file and scale it to fit within the specified canvas size.
    The SVG will be placed at a random position inside the canvas.

    Parameters:
    svg_path (str): Path to the SVG file.
    canvas_width (int): Width of the target canvas.
    canvas_height (int): Height of the target canvas.

    Returns:
    PIL.Image, tuple: The converted and scaled stencil image and the bounding box of the logo.
    """
    try:
        size = get_svg_size(svg_path)
        scale = compute_stencil_scale_factor((canvas_width, canvas_height), size)
        scale = scale * (random.random() * .6 + .35)

        png_data = cairosvg.svg2png(url=svg_path, scale=scale)
        stencil = Image.open(BytesIO(png_data))

        stencil_width, stencil_height = stencil.size

        # Generate random position
        pad_left = random.randint(0, canvas_width - stencil_width)
        pad_top = random.randint(0, canvas_height - stencil_height)

        # Create a new image with the same size as canvas and paste the stencil at a random position
        stencil_padded = Image.new("RGBA", (canvas_width, canvas_height), 0)  # Assuming stencil is grayscale (L mode)
        stencil_padded.paste(stencil, (pad_left, pad_top))

        # Calculate bounding box
        bounding_box = ((pad_left, pad_top), (pad_left + stencil_width, pad_top + stencil_height))

        return stencil_padded, bounding_box

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def apply_stencil(image1, image2, stencil):
    """
    Apply a stencil image to overlay image2 onto image1.

    Parameters:
    image1 (PIL.Image): The base image.
    image2 (PIL.Image): The image to overlay.
    stencil (PIL.Image): The stencil image.

    Returns:
    PIL.Image: The resulting image after applying the stencil.
    """
    # Ensure the first two images are the same size
    if image1.size != image2.size:
        raise ValueError("The first two images must be of the same size.")

    # Create a new image for the result
    result = image1.copy()

    # Paste the second image onto the first using the stencil as a mask
    result.paste(image2, (0, 0), stencil)

    return result


def get_svg_size(svg_path):
    """
    Get the size of an SVG file.

    Parameters:
    svg_path (str): Path to the SVG file.

    Returns:
    tuple: Width and height of the SVG.
    """
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # The SVG namespace
        namespace = {'svg': 'http://www.w3.org/2000/svg'}

        # Get the width and height attributes
        width = root.attrib.get('width')
        height = root.attrib.get('height')

        if width is None or height is None:
            # If width and height are not directly specified, try to get the viewBox attribute
            viewBox = root.attrib.get('viewBox')
            if viewBox:
                _, _, width, height = viewBox.split()

        # Convert width and height to float
        width = float(width)
        height = float(height)

        return width, height

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def create_card_background_with_big_logo(svg_path, width, height):
    """
    Create a card background with a big logo using randomly generated backgrounds and color palettes.

    Parameters:
    svg_path (str): Path to the SVG file for the logo.
    width (int): Width of the card background.
    height (int): Height of the card background.

    Returns:
    PIL.Image, tuple: The final card background image with the big logo applied and the bounding box of the logo.
    """
    palette = generate_random_palette()

    complementary_colors = [palette['Complementary']] + palette['Triadic']
    complementary = random.choice([palette['Complementary']] + palette['Triadi-c'])

    analogous_colors = palette['Analogous'] + [palette['Primary']]
    primary = palette['Primary']

    background_a = generate_random_background(
        width=width, height=height, primary_color=primary, accent_colors=analogous_colors
    )

    background_b = generate_random_background(
        width=width, height=height, primary_color=complementary, accent_colors=complementary_colors
    )

    stencil, bounding_box = convert_svg_to_png(svg_path, width, height)

    if stencil is not None:
        result_image = apply_stencil(background_a, background_b, stencil)
        return result_image, bounding_box
    else:
        raise ValueError("Failed to convert SVG to PNG and create stencil.")


if __name__ == "__main__":
    # Example usage
    svg_path = 'HSBC.svg'
    width = 900
    height = 540
    result_image, bounding_box = create_card_background_with_big_logo(svg_path, width, height)
    result_image.save('result.png')

    print(f"Bounding box of the logo: {bounding_box}")
