import json

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageDraw


def load_image(image_path):
    """Load an image from the given path."""
    return cv2.imread(image_path)


def preprocess_image(image):
    """Convert the image to grayscale, apply thresholding, and enhance contrast."""
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)

    height, width = binary_image.shape[:2]
    binary_image = cv2.resize(binary_image, np.array((width, height)) * 2, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("../binary_image.png", binary_image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    gray_image = cv2.resize(gray_image, np.array((width, height)) * 2, interpolation=cv2.INTER_CUBIC)
    contrast_image = clahe.apply(gray_image)

    cv2.imwrite("../contrast_image.png", contrast_image)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    contrast_image = cv2.filter2D(contrast_image, -1, kernel)

    return contrast_image


def perform_ocr(image):
    """Perform OCR on the given image and return the data."""
    pil_image = Image.fromarray(image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    data = pytesseract.image_to_data(
        pil_image,
        output_type=pytesseract.Output.DICT,
        config="--psm 1"
    )

    return data


def convert_to_relative_coordinates(data, img_width, img_height):
    """Convert absolute coordinates to relative coordinates (0 to 1)."""
    n_boxes = len(data['level'])
    text_coordinates = []
    for i in range(n_boxes):
        if data['text'][i].strip():
            x = data['left'][i] / img_width
            y = data['top'][i] / img_height
            w = data['width'][i] / img_width
            h = data['height'][i] / img_height

            text_coordinates.append({
                "text": data['text'][i],
                "coordinates": [x, y, x + w, y + h],
                "coordinates_in_pixels": [data['left'][i], data['top'][i]],
                "width": w,
                "height": h
            })
    return text_coordinates


def draw_bounding_boxes(image, text_coordinates):
    """Draw bounding boxes around detected text on the image."""
    img_width, img_height = image.size
    draw = ImageDraw.Draw(image)

    for item in text_coordinates:
        x1 = int(item["coordinates"][0] * img_width)
        y1 = int(item["coordinates"][1] * img_height)
        x2 = int(item["coordinates"][2] * img_width)
        y2 = int(item["coordinates"][3] * img_height)
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    return image


def save_and_show_image(image_with_boxes, output_path="output_with_boxes.png"):
    """Save and display the image with bounding boxes."""
    image_with_boxes.save(output_path)
    image_with_boxes.show()


def consolidate_words(text_coordinates, space_factor=1, max_spaces=6):
    """
    Consolidates words that are meant to be together based on their horizontal proximity and y-coordinate alignment.

    Parameters:
    - text_coordinates (list): List of dictionaries containing 'text', 'coordinates', 'width', and 'height' keys.
    - space_factor (float): Multiplier for the height of the word to define reasonable space width.
    - max_spaces (int): Maximum number of white spaces allowed between words.

    Returns:
    - list: List of consolidated text with updated coordinates, width, and height.
    """
    if not text_coordinates:
        return []

    consolidated = []
    current_phrase = text_coordinates[0]['text']
    current_coords = text_coordinates[0]['coordinates']
    current_width = text_coordinates[0]['width']
    current_height = text_coordinates[0]['height']

    for i in range(1, len(text_coordinates)):
        word = text_coordinates[i]['text']
        coords = text_coordinates[i]['coordinates']
        word_width = text_coordinates[i]['width']
        word_height = text_coordinates[i]['height']

        # Calculate horizontal distance between words
        previous_right_edge = current_coords[2]
        next_left_edge = coords[0]
        distance = next_left_edge - previous_right_edge

        # Calculate vertical alignment difference
        vertical_alignment_diff = abs(current_coords[1] - coords[1])

        # Reasonable white space based on word height
        reasonable_space = min(current_height, word_height) * space_factor

        # Check if words are close enough to be part of the same phrase
        if distance <= max_spaces * reasonable_space and vertical_alignment_diff <= word_height * 0.5:
            current_phrase += " " + word
            current_coords[2] = coords[2]  # Update the right edge of the bounding box
            current_coords[3] = max(current_coords[3], coords[3])  # Update the bottom edge if needed
            current_width += word_width  # Update the width
            current_height = max(current_height, word_height)  # Update the height
        else:
            # Words are too far apart, finalize the current phrase and start a new one
            consolidated.append({
                'text': current_phrase,
                'coordinates': current_coords,
                'width': current_width,
                'height': current_height
            })
            current_phrase = word
            current_coords = coords
            current_width = word_width
            current_height = word_height

    # Append the last phrase
    consolidated.append({
        'text': current_phrase,
        'coordinates': current_coords,
        'width': current_width,
        'height': current_height
    })

    return consolidated


def main(image_path):
    """Main function to process the image and perform OCR."""
    image = load_image(image_path)
    img_height, img_width = image.shape[:2]
    preprocessed_image = preprocess_image(image)
    ocr_data = perform_ocr(preprocessed_image)
    text_coordinates = convert_to_relative_coordinates(ocr_data, img_width, img_height)
    consolidated_text_coordinates = consolidate_words(text_coordinates, max_spaces=4)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # image_with_boxes = draw_bounding_boxes(pil_image, text_coordinates)
    # save_and_show_image(image_with_boxes)
    print(text_coordinates)
    return consolidated_text_coordinates


if __name__ == "__main__":
    image_path = '../../assets/templates/template_2.png'  # Replace with the path to your image
    consolidated_text_coordinates = main(image_path)
    print(json.dumps(consolidated_text_coordinates, indent=4))
