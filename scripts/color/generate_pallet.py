import colorsys

from .generate_color import generate_random_color


def rgb_to_hls(r, g, b):
    return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)


def hls_to_rgb(h, l, s):
    return tuple(round(i * 255) for i in colorsys.hls_to_rgb(h, l, s))


def adjust_lightness(color, factor):
    h, l, s = rgb_to_hls(*color)
    return hls_to_rgb(h, max(0, min(1, l * factor)), s)


def compute_analogous_colors(color, separation=.07):
    h, l, s = rgb_to_hls(*color)
    return [hls_to_rgb((h + separation) % 1.0, l, s), hls_to_rgb((h - separation) % 1.0, l, s)]


def compute_complementary_color(color):
    h, l, s = rgb_to_hls(*color)
    h = (h + 0.5) % 1.0
    return hls_to_rgb(h, l, s)


def triadic_colors(color):
    h, l, s = rgb_to_hls(*color)
    return [hls_to_rgb((h + 1 / 3) % 1.0, l, s), hls_to_rgb((h + 2 / 3) % 1.0, l, s)]


class ColorPalette:
    def __init__(self, primary_color=None):
        self.primary = primary_color if primary_color is not None else generate_random_color()

    def get_primary_group(self, separation=0.025):
        return [self.primary] + compute_analogous_colors(self.primary, separation)

    def get_close_analogous(self, separation=0.025):
        return compute_analogous_colors(self.primary, separation)

    def get_analogous(self, separation=0.095):
        return compute_analogous_colors(self.primary, separation)

    def get_complementary(self):
        return compute_complementary_color(self.primary)

    def get_close_complementary(self, separation=0.025):
        complementary = self.get_complementary()
        return compute_analogous_colors(complementary, separation)

    def get_complementary_group(self, separation=0.025):
        complementary = self.get_complementary()
        return [complementary] + self.get_close_complementary(separation)

    def get_triadic(self):
        return triadic_colors(self.primary)

    def to_dict(self):
        return {
            "primary": self.primary,
            "primary_group": self.get_primary_group(),
            "analogous": self.get_analogous(),
            "close_analogous": self.get_close_analogous(),
            "complementary": self.get_complementary(),
            "close_complementary": self.get_close_complementary(),
            "triadic": self.get_triadic(),
            "complementary_group": self.get_complementary_group()
        }
