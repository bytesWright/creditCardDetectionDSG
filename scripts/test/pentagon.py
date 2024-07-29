import random

import cv2
import numpy as np


def draw_tiling_pattern_cv2(image_size=(400, 400), tile_size=40):
    """
    Draw a tiling pattern using OpenCV.

    Parameters:
    - image_size: Size of the output image (width, height).
    - tile_size: Size of each tile.
    """
    width, height = image_size
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Loop to create the pattern
    for i in range(0, width, tile_size):
        for j in range(0, height, tile_size):
            # Define the tile bounding box
            top_left = (i, j)
            bottom_right = (i + tile_size, j + tile_size)

            # Draw the tile outline
            cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), 1)
            cv2.rectangle(img, top_left, bottom_right, (random.randint(0, 150), 211, 211), -1)  # Fill the tile

            # Draw diagonal lines inside the tile
            cv2.line(img, top_left, (i + tile_size, j + tile_size), (random.randint(0, 150), 211, 211), 1)
            cv2.line(img, (i + tile_size, j), (i, j + tile_size), (random.randint(0, 150), random.randint(200,205), random.randint(200,205)), 1)

    cv2.imshow('Tiling Pattern', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Example usage
draw_tiling_pattern_cv2(image_size=(400, 400), tile_size=40)
