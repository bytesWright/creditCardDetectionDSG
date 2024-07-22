from matplotlib import pyplot as plt

from scripts.color.conversion import rgb_to_hex


def visualize_palette(palette):
    fig, ax = plt.subplots(figsize=(12, 2))
    current_index = 0
    for name, colors in palette.items():
        if isinstance(colors, tuple):
            colors = [colors]
        for color in colors:
            ax.add_patch(plt.Rectangle((current_index, 0), 2, 1, color=[c / 255.0 for c in color]))
            ax.text(current_index + 1, -0.1, name, ha='center', va='center', fontsize=8, color='black')
            ax.text(current_index + 1, -0.25, str(color), ha='center', va='center', fontsize=8, color='black')
            current_index += 2
    ax.set_xlim(0, current_index)
    ax.set_ylim(-0.3, 1)
    ax.axis('off')
    plt.show()


def print_random_palette_hex(palette):
    for name, colors in palette.items():
        if isinstance(colors, tuple):
            colors = [colors]
        for color in colors:
            hex_color = rgb_to_hex(color)
            print(f"{name}: {hex_color}")