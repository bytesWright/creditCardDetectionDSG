import math
import random

from PIL import Image, ImageDraw


def generate_stacked_triangles(area_width, area_height, triangle_width=50, triangle_height=100):
    """Generate coordinates for stacked triangles within a specified area.

    Parameters:
    - area_width: Width of the area to cover with triangles.
    - area_height: Height of the area to cover with triangles.
    - triangle_width: Width of the triangles.
    - triangle_height: Height of the triangles.

    Yields:
    - List of coordinates for each triangle.
    """
    for x in range(-1, int(area_width / triangle_width) + 1):
        for y in range(int(area_height / triangle_height)):
            # Add a horizontal offset on odd numbered rows
            x_ = x * triangle_width if (y % 2 == 0) else (x + 0.5) * triangle_width

            # Coordinates of two triangles forming a parallelogram
            yield [(x_, y * triangle_height),
                   (x_ + triangle_width, y * triangle_height),
                   (x_ + triangle_width / 2, (y + 1) * triangle_height)]
            yield [(x_ + triangle_width, y * triangle_height),
                   (x_ + 1.5 * triangle_width, (y + 1) * triangle_height),
                   (x_ + triangle_width / 2, (y + 1) * triangle_height)]


def generate_stacked_hexagons(area_width, area_height, hexagon_width=30, hexagon_height=30):
    """Generate coordinates for stacked hexagons within a specified area.

    Parameters:
    - area_width: Width of the area to cover with hexagons.
    - area_height: Height of the area to cover with hexagons.
    - hexagon_width: Width of the hexagons (distance between two parallel sides).
    - hexagon_height: Height of the hexagons (distance between two opposite vertices).

    Yields:
    - List of coordinates for each hexagon.
    """
    hex_radius = hexagon_width / 2
    hex_height = hexagon_height
    row_height = 3 / 4 * hex_height

    def hex_corner(center_x, center_y, i):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        return (center_x + hex_radius * math.cos(angle_rad), center_y + hex_radius * math.sin(angle_rad))

    for y in range(int(area_height / row_height) + 1):
        for x in range(int(area_width / hexagon_width) + 1):
            center_x = x * hexagon_width * 3 / 4
            center_y = y * row_height

            if y % 2 == 1:
                center_x += hexagon_width / 2

            hexagon = [hex_corner(center_x, center_y, i) for i in range(6)]
            yield hexagon


def draw_tiling(coord_generator, filename):
    """
    Given a coordinate generator and a filename, render those coordinates
    in a new image and save them to the file.
    """
    canvas_width = 400
    canvas_height = 400

    im = Image.new(mode='RGB', size=(canvas_width, canvas_height))
    draw = ImageDraw.Draw(im)

    for shape in coord_generator(canvas_width, canvas_height):
        draw.polygon(
            shape,
            outline=(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            ),
            fill=(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )
        )

    im.save(filename)


if __name__ == '__main__':
    # draw_tiling(generate_stacked_hexagons, filename='squares.png')
    draw_tiling(generate_stacked_triangles, filename='triangles.png')
    # draw_tiling(generate_stacked_hexagons, filename='hexagons.png')
