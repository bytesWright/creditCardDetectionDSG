import math
import random

import numpy as np
from PIL import Image, ImageDraw

from scripts.color.generate_color import generate_random_shade_color


def linear_gradient(base_color, width, height):
    start_color = generate_random_shade_color(base_color)
    end_color = generate_random_shade_color(base_color)
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    for i in range(height):
        blend = i / height
        r = int(start_color[0] * (1 - blend) + end_color[0] * blend)
        g = int(start_color[1] * (1 - blend) + end_color[1] * blend)
        b = int(start_color[2] * (1 - blend) + end_color[2] * blend)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    return image


def radial_gradient(base_color, width, height):
    center_color = generate_random_shade_color(base_color)
    edge_color = generate_random_shade_color(base_color)
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Random center point
    cx, cy = random.randint(0, width), random.randint(0, height)

    # Maximum distance from the center to a corner
    max_radius = max(
        ((cx - 0) ** 2 + (cy - 0) ** 2) ** 0.5,
        ((cx - width) ** 2 + (cy - 0) ** 2) ** 0.5,
        ((cx - 0) ** 2 + (cy - height) ** 2) ** 0.5,
        ((cx - width) ** 2 + (cy - height) ** 2) ** 0.5,
    )

    for r in range(int(max_radius), 0, -1):
        blend = r / max_radius
        r_color = int(center_color[0] * blend + edge_color[0] * (1 - blend))
        g_color = int(center_color[1] * blend + edge_color[1] * (1 - blend))
        b_color = int(center_color[2] * blend + edge_color[2] * (1 - blend))
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(r_color, g_color, b_color))
    return image


def solid_color(base_color, width, height):
    color = generate_random_shade_color(base_color)
    image = Image.new('RGB', (width, height), color)
    return image


def generate_random_base(width, height, base_color):
    background_type = random.choice(['linear', 'radial', 'solid'])

    if background_type == 'linear':
        return linear_gradient(base_color, width, height)
    elif background_type == 'radial':
        return radial_gradient(base_color, width, height)
    elif background_type == 'solid':
        return solid_color(base_color, width, height)


def draw_curved_lines(image, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)

    def random_thickness():
        return random.randint(height // 60, height // 5)

    def bezier_curve(p0, p1, p2, p3, t):
        return (
                (1 - t) ** 3 * np.array(p0) +
                3 * (1 - t) ** 2 * t * np.array(p1) +
                3 * (1 - t) * t ** 2 * np.array(p2) +
                t ** 3 * np.array(p3)
        )

    def random_curve_points():
        return [
            (0, random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (width, random.randint(0, height))
        ]

    num_lines = random.randint(0, 30)
    thickness = random_thickness()

    for _ in range(num_lines):
        points = random_curve_points()
        curve_points = [bezier_curve(points[0], points[1], points[2], points[3], t) for t in np.linspace(0, 1, 1000)]
        curve_points = [(int(x), int(y)) for x, y in curve_points]

        draw.line(curve_points, fill=color, width=thickness)

    return image


def draw_straight_lines(image, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)

    def random_thickness():
        return random.randint(height // 60, height // 5)

    def random_line_points():
        return [
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height))
        ]

    num_lines = random.randint(5, 15)

    for _ in range(num_lines):
        thickness = random_thickness()
        points = random_line_points()
        draw.line(points, fill=color, width=thickness)

    return image


def draw_random_spots(image, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)

    def random_spot_size():
        return random.randint(height // 30, height // 10)

    num_spots = random.randint(10, 100)

    for _ in range(num_spots):
        spot_size = random_spot_size()
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.ellipse([
            (x - spot_size, y - spot_size), (x + spot_size, y + spot_size)
        ], fill=color)

    return image


def draw_random_triangles(image, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)

    def random_triangle_points():
        return [
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height)),
            (random.randint(0, width), random.randint(0, height))
        ]

    num_triangles = random.randint(5, 30)

    for _ in range(num_triangles):
        points = random_triangle_points()
        draw.polygon(points, fill=color)

    return image


def draw_parallel_lines(image, color):
    width, height = image.size
    draw = ImageDraw.Draw(image)

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

    return image


def draw_random_details(image, color, contrast_range=.25):
    color = generate_random_shade_color(color, contrast_range)

    detail_type = random.choice(['straight', 'curved', 'spots', 'triangles', 'parallel'])

    if detail_type == 'straight':
        return draw_straight_lines(image, color)
    elif detail_type == 'curved':
        return draw_curved_lines(image, color)
    elif detail_type == 'spots':
        return draw_random_spots(image, color)
    elif detail_type == 'triangles':
        return draw_random_triangles(image, color)
    elif detail_type == 'parallel':
        return draw_parallel_lines(image, color)


def draw_random_detail(image, colors, contrast_range=.25):
    color = random.choice(colors)
    image = draw_random_details(image, color, contrast_range)

    while random.random() > .5:
        color = random.choice(colors)
        image = draw_random_details(image, color, contrast_range)

    return image


def generate_random_background(width, height, primary_color, accent_colors=None):
    if accent_colors is None:
        accent_colors = [primary_color]

    base = generate_random_base(width, height, primary_color)
    return draw_random_detail(base, accent_colors)
