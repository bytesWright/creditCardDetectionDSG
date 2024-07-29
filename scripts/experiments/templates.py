import inspect

from PIL import Image, ImageDraw, ImageFont

from scripts import templates


def display_images_in_grid(images_with_modules, n_columns, spacing=10, font_size=14):
    # Load default font for module names
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the size of the grid
    n_rows = (len(images_with_modules) + n_columns - 1) // n_columns
    widths, heights = zip(
        *(img_dict["image"].size for img_dict in images_with_modules)
    )

    max_width = max(widths)
    max_height = max(heights) + font_size + spacing

    # Create a new blank image with appropriate size
    grid_width = n_columns * (max_width + spacing) - spacing
    grid_height = n_rows * (max_height + spacing) - spacing
    grid_image = Image.new('RGBA', (grid_width, grid_height), color='white')

    draw = ImageDraw.Draw(grid_image)

    # Paste each image into the grid image and add module name
    for index, img_dict in enumerate(images_with_modules):
        row, col = divmod(index, n_columns)
        x = col * (max_width + spacing)
        y = row * (max_height + spacing)

        grid_image.paste(img_dict["image"], (x, y))

        # Draw the module name below the image
        text_x = x + (max_width / 2)
        text_y = y + img_dict["image"].height + spacing // 2
        module_name = img_dict["member"]
        bbox = draw.textbbox((0, 0), module_name, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((text_x - text_width / 2, text_y), module_name, fill="black", font=font)

    grid_image.show()


def is_template_function(name, member):
    return "template" in name and inspect.isfunction(member)


def call_template_function(function):
    try:
        result = function()
        if isinstance(result, tuple) and len(result) > 0 and isinstance(result[0], Image.Image):
            return result[0]
    except Exception as e:
        print(f"Error calling function {function.__name__}: {e}")
    return None


def collect_template_images(module):
    images = []

    for name, member in inspect.getmembers(module):
        if is_template_function(name, member):
            image = call_template_function(member)
            if image:
                images.append({"member": member.__name__, "image": image})

    return images


images = collect_template_images(templates)
display_images_in_grid(images, 4)
