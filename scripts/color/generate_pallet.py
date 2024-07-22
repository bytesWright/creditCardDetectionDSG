import colorsys

from .generate_color import generate_random_color


def generate_color_palette(primary_color):
    def rgb_to_hls(r, g, b):
        return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    def hls_to_rgb(h, l, s):
        return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))

    def adjust_lightness(color, factor):
        h, l, s = rgb_to_hls(*color)
        return hls_to_rgb(h, max(0, min(1, l * factor)), s)

    def complementary_color(color):
        h, l, s = rgb_to_hls(*color)
        h = (h + 0.5) % 1.0
        return hls_to_rgb(h, l, s)

    def analogous_colors(color):
        h, l, s = rgb_to_hls(*color)
        return [hls_to_rgb((h + 0.05) % 1.0, l, s), hls_to_rgb((h - 0.05) % 1.0, l, s)]

    def triadic_colors(color):
        h, l, s = rgb_to_hls(*color)
        return [hls_to_rgb((h + 1 / 3) % 1.0, l, s), hls_to_rgb((h + 2 / 3) % 1.0, l, s)]

    primary_rgb = primary_color
    palette = {
        "Primary": primary_rgb,
        "Complementary": complementary_color(primary_rgb),
        "Analogous": analogous_colors(primary_rgb),
        "Triadic": triadic_colors(primary_rgb)
    }

    return palette


def generate_random_palette():
    primary_color = generate_random_color()
    palette = generate_color_palette(primary_color)
    return palette
