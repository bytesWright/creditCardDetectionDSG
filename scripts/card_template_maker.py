import json
import os

import cv2
import easyocr
from termcolor import colored


def display_image_with_bbox(image_path, coordinates, text):
    image = cv2.imread(image_path)
    x0, y0 = coordinates[0]
    x1, y1 = coordinates[2]
    cv2.rectangle(image, (x0, y0), (x1, y1), (0, 255, 0), 2)
    cv2.putText(image, text, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.imwrite('image.png', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def consolidate_words(elements, y_threshold=10, x_threshold=20):
    consolidated_elements = []
    current_line = []

    def sort_by_x(item):
        return item["coordinates"][0]

    def sort_by_y(item):
        return item["coordinates"][1]

    elements.sort(key=sort_by_y)

    for item in elements:
        coordinates = item["coordinates"]
        text = item["text"]
        item_type = item["type"]

        x1, y1 = coordinates[0], coordinates[1]

        if not current_line:
            current_line.append(item)
            continue

        last_item = current_line[-1]
        last_coordinates = last_item["coordinates"]
        last_x1, last_y1 = last_coordinates[0], last_coordinates[1]
        last_type = last_item["type"]

        if abs(y1 - last_y1) <= y_threshold and item_type == last_type:
            current_line.append(item)
        else:
            current_line.sort(key=sort_by_x)
            combined_text = " ".join([word["text"] for word in current_line])
            combined_confidence = sum([word["confidence"] for word in current_line]) / len(current_line)
            combined_coordinates = [
                current_line[0]["coordinates"][0],
                current_line[0]["coordinates"][1],
                current_line[-1]["coordinates"][2],
                current_line[0]["coordinates"][3]
            ]
            consolidated_elements.append({
                "text": combined_text,
                "coordinates": combined_coordinates,
                "confidence": combined_confidence,
                "type": current_line[0]["type"]
            })
            current_line = [item]

    if current_line:
        current_line.sort(key=sort_by_x)
        combined_text = " ".join([word["text"] for word in current_line])
        combined_confidence = sum([word["confidence"] for word in current_line]) / len(current_line)
        combined_coordinates = [
            current_line[0]["coordinates"][0],
            current_line[0]["coordinates"][1],
            current_line[-1]["coordinates"][2],
            current_line[0]["coordinates"][3]
        ]
        consolidated_elements.append({
            "text": combined_text,
            "coordinates": combined_coordinates,
            "confidence": combined_confidence,
            "type": current_line[0]["type"]
        })

    return consolidated_elements


def filter_and_correct_easyocr_output(image_path, easyocr_output):
    filtered_corrected_output = []
    type_options = {
        '1': 'text',
        '2': 'creditCardNumber',
        '3': 'userName',
        '4': 'expirationDate',
        '5': 'cvc',
        '6': 'cardTypeLogo',
        '7': 'paymentNetworkLogo',
        '8': 'bankName',
        '9': 'benefit',
        '10': 'cardFlavor',
        '11': 'domain',
        '12': "entityPhoneNumber"
    }

    for item in easyocr_output:
        coordinates, text, confidence = item
        display_image_with_bbox(image_path, coordinates, text)

        print(colored(f"Text: '{text}', Confidence: {confidence:.2f}", 'cyan'))
        keep = input(f"[{text}] Keep this item [{confidence:.2f}]? (y/n): ")
        if keep.lower() == 'n':
            continue

        corrected_text = input(f"Is this the right word? (Leave empty to keep as is): '{text}': ")
        if corrected_text:
            text = corrected_text

        print("Specify the type:")
        print_dict_in_columns(type_options, 4)

        item_type_num = input("Enter the number corresponding to the type: ")
        while item_type_num not in type_options:
            item_type_num = input("Invalid input. Enter the number corresponding to the type: ")

        item_type = type_options[item_type_num]

        filtered_corrected_output.append({
            "text": text,
            "coordinates": [
                int(coordinates[0][0]),
                int(coordinates[0][1]),
                int(coordinates[2][0]),
                int(coordinates[2][1])
            ],
            "confidence": confidence,
            "type": item_type
        })

    return consolidate_words(filtered_corrected_output)


def transform_coordinates_to_percentage(template, image):
    # Read the image to get its dimensions
    image_height, image_width = image.shape[:2]

    # Add the form factor to the main level of the result dictionary
    template['formFactor'] = {'width': image_width, 'height': image_height}

    for element in template['elements']:
        x0, y0, x1, y1 = element['coordinates']
        element_width = x1 - x0
        element_height = y1 - y0

        element['coordinates'] = [
            (x0 / image_width),
            (y0 / image_height),
            (x1 / image_width),
            (y1 / image_height)
        ]

        element['height'] = (element_height / image_height)
        element['width'] = (element_width / image_height)

    return template


def get_template_count(path):
    if not os.path.exists(path):
        return 0
    with open(path, 'r') as file:
        return int(file.read())


def update_template_count(path, count):
    with open(path, 'w') as file:
        file.write(str(count))


def get_user_inputs():
    print("Specify the template type:")
    print("1: front")
    print("2: back")
    print("3: custom")

    template_type_options = {'1': 'front', '2': 'back', '3': 'custom'}
    template_type_num = input("Enter the number corresponding to the template type: ")
    while template_type_num not in template_type_options:
        template_type_num = input("Invalid input. Enter the number corresponding to the template type: ")
    template_type = template_type_options[template_type_num]

    return template_type


def save_template(template, template_count, templates_dir, image):
    template_file_path = os.path.join(templates_dir, f"template_{template_count}.json")
    with open(template_file_path, 'w') as template_file:
        json.dump(template, template_file, indent=4)

    template_file_path = os.path.join(templates_dir, f"template_{template_count}.jpg")
    cv2.imwrite(template_file_path, image)

    print(f"Template saved as {template_file_path}")


def print_dict_in_columns(data, num_columns):
    keys = list(data.keys())
    values = list(data.values())

    max_key_len = max(len(str(k)) for k in keys)
    max_val_len = max(len(str(v)) for v in values)

    # Determine the column width based on the maximum key and value lengths
    col_width = max_key_len + max_val_len + 4

    for i in range(0, len(keys), num_columns):
        for j in range(num_columns):
            index = i + j
            if index < len(keys):
                key = keys[index]
                value = values[index]
                print(f"{key}: {value}".ljust(col_width), end="")
        print()  # Newline after printing the row


def main():
    template_type, complementary = get_user_inputs()

    reader = easyocr.Reader(['en'])
    image_path = '../assets/templates/template_2.png'  # Replace with your image path
    result = reader.readtext(image_path)
    elements = filter_and_correct_easyocr_output(image_path, result)

    template = {
        'type': template_type,
        'elements': elements
    }

    image = cv2.imread(image_path)
    transform_coordinates_to_percentage(template, image)

    templates_dir = "../assets/templates/"
    counter_file_path = os.path.join(templates_dir, "counter.txt")
    os.makedirs(templates_dir, exist_ok=True)

    template_count = get_template_count(counter_file_path)
    template_count += 1
    update_template_count(counter_file_path, template_count)

    save_template(template, template_count, templates_dir, image)


if __name__ == "__main__":
    main()
