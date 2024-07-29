import os

# noinspection PyUnresolvedReferences
import pillow_avif
from PIL import Image


def convert_images(folder_path, destination):
    # Supported extensions
    extensions = ['png', 'webp', 'avif', 'jpg']

    # Iterate over the files in the given folder
    for i, filename in enumerate(os.listdir(folder_path)):
        # Check if the file is an image with one of the specified extensions
        print(f"Converting {filename}")

        file_path = os.path.join(folder_path, filename)
        # Open the image

        with Image.open(file_path) as img:
            # Convert the image to RGB mode if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            output_path = os.path.join(destination, f"{i}.jpg")
            img.save(output_path, 'JPEG')

            print(f"    -> {output_path}")


# Example usage
folder_path = '../../assets/images/real_cards/source'
convert_images(folder_path, '../../assets/images/real_cards/')
