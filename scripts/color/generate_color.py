import random


def generate_random_shade_color(base_color, color_range=.15):
    factor = random.uniform(-color_range / 2, color_range / 2)

    return tuple(
        min(
            max(
                0,
                int(
                    base_color[i] * (1 + factor)
                )
            ),
            255
        )
        for i in range(3)
    )


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return r, g, b
