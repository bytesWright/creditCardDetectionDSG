import math
import random

import numpy as np
from PIL import ImageDraw, Image


def draw_curved_lines(image, primary_colors, complementary_colors, **parameters):
    color = random.choice(primary_colors)
    width, height = image.size
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer, "RGBA")

    def random_thickness():
        return random.randint(height // 60, height // 5)

    def bezier_curve(p0, p1, p2, p3, t):
        return (
                (1 - t) ** 3 * np.array(p0)
                + 3 * (1 - t) ** 2 * t * np.array(p1)
                + 3 * (1 - t) * t ** 2 * np.array(p2)
                + t ** 3 * np.array(p3)
        )

    def random_curve_points():
        return [
            (0, random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (width, random.randint(0, height)),
        ]

    num_lines = random.randint(0, 30)
    thickness = random_thickness()

    for _ in range(num_lines):
        points = random_curve_points()
        curve_points = [
            bezier_curve(points[0], points[1], points[2], points[3], t)
            for t in np.linspace(0, 1, 1000)
        ]
        curve_points = [(int(x), int(y)) for x, y in curve_points]

        draw.line(curve_points, fill=color, width=thickness)

    image.paste(transparent_layer, (0, 0), transparent_layer)
    return image


def draw_random_rectangles(image, primary_colors, complementary_colors, **parameters):
    color = random.choice(primary_colors)
    width, height = image.size
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer, "RGBA")

    def random_thickness():
        return random.randint(height // 60, height // 5)

    def random_line_points():
        return [
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
        ]

    num_lines = random.randint(5, 15)

    for _ in range(num_lines):
        thickness = random_thickness()
        points = random_line_points()
        draw.line(points, fill=color, width=thickness)

    image.paste(transparent_layer, (0, 0), transparent_layer)
    return image


def draw_random_spots(image, primary_colors, complementary_colors, **parameters):
    color = random.choice(primary_colors)
    width, height = image.size
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer, "RGBA")

    def random_spot_size():
        return random.randint(height // 30, height // 10)

    num_spots = random.randint(10, 100)

    for _ in range(num_spots):
        spot_size = random_spot_size()
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse(
            [(x - spot_size, y - spot_size), (x + spot_size, y + spot_size)],
            fill=color,
        )

    image.paste(transparent_layer, (0, 0), transparent_layer)
    return image


def draw_random_triangles(image, primary_colors, complementary_colors, **parameters):
    color = random.choice(primary_colors)

    width, height = image.size
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer, 'RGBA')

    def random_triangle_points():
        return [
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height))
        ]

    num_triangles = random.randint(2, 15)

    for _ in range(num_triangles):
        points = random_triangle_points()
        draw.polygon(points, fill=color)

    # otherwise the transparency don't work
    image.paste(transparent_layer, (0, 0), transparent_layer)
    return image


def draw_parallel_lines(image, primary_colors, complementary_colors, **parameters):
    color = random.choice(primary_colors)
    width, height = image.size
    transparent_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(transparent_layer, 'RGBA')

    def random_thickness():
        return random.randint(height // 40, height // 30)

    def random_spacing():
        return random.randint(20, 40)

    angle = random.uniform(0, math.pi)
    spacing = random_spacing()
    thickness = random_thickness()

    for i in range(-height, width + height, spacing):
        x1 = i
        y1 = 0
        x2 = i + height * math.tan(angle)
        y2 = height
        draw.line([(x1, y1), (x2, y2)], fill=color, width=thickness)

    image.paste(transparent_layer, (0, 0), transparent_layer)
    return image


draw_details_functions = {
    'draw_random_rectangles': draw_random_rectangles,
    'draw_curved_lines': draw_curved_lines,
    'draw_random_spots': draw_random_spots,
    'draw_random_triangles': draw_random_triangles,
    'draw_parallel_lines': draw_parallel_lines
}
