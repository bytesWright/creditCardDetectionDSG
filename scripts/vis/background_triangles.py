import math
import random

from PIL import Image, ImageDraw

from scripts.color import generate_random_shade_color
from scripts.color.generate_pallet import generate_random_palette


def g(x, y, w=1, h=1):
    a = y % 2
    return round(
        h * abs(
            math.sin(math.pi * x / w + math.pi * a / 2)
        ), 5
    ) + y * h


def triangle_points(row, col, width=1, height=1):
    x = col * width / 2
    x2 = (x + width / 2)
    x3 = (x + width)

    y1 = g(x, row, width, height)
    y2 = g(x2, row, width, height)
    y3 = g(x3, row, width, height)

    return (
        (row, col),
        (x, y1),
        (x2, y2),
        (x3, y3)
    )


def generate_triangles(area_width, area_height, triangle_width=10, triangle_height=10):
    triangles = []
    cols = math.ceil(area_width / (triangle_width / 2))
    rows = math.ceil(area_height / triangle_height)

    for r in range(-1, rows):
        for c in range(-1, cols):
            triangle = triangle_points(r, c, triangle_width, triangle_height)
            triangles.append(triangle)

    return (cols, rows), triangles


def draw_triangles(image, triangles, primary_colors, complementary_colors, separation_line):
    draw = ImageDraw.Draw(image)

    for triangle in triangles:
        (row, col) = triangle[0]
        points = triangle[1:]

        separation_col = separation_line[row]
        color = random.choice(primary_colors)

        if col > separation_col:
            color = random.choice(complementary_colors)

        color = generate_random_shade_color(color)

        draw.polygon(points, fill=color)  # Skip (row, col) tuple for drawing


def generate_separation(rows, cols):
    r = 0
    c = random.randint(0, cols)
    result = [c]

    while r <= rows:
        r += 1
        step = random.randint(-2, 2)
        c += step

        if c < -1:
            c = -1
        if c > cols:
            c = cols

        result.append(c)
    return result


if __name__ == "__main__":
    # Example usage:
    area_width = 400
    area_height = 400
    triangle_width = 50
    triangle_height = 50

    image = Image.new("RGB", (area_width, area_height), (0, 0, 0))
    (rows, cols), triangles = generate_triangles(area_width, area_height, triangle_width, triangle_height)

    separation_line = generate_separation(rows, cols)

    palette = generate_random_palette()

    # primary_colors = palette['Analogous'] + [palette['Primary']]
    # complementary_colors = [palette['Complementary']] + palette['Triadic']

    # primary_colors = [palette['Primary']]
    # complementary_colors = [palette['Complementary']]

    primary_colors = palette['Analogous']
    complementary_colors = [palette['Primary']]

    draw_triangles(
        image,
        triangles,
        primary_colors,
        complementary_colors,
        separation_line
    )

    image.show()
