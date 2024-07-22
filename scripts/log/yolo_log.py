from scripts.log.objects_classes import classes_to_ids


def create_yolo_description(objects, image_width, image_height):
    yolo_description = []

    for obj in objects:
        obj_type = obj['type']
        bbox = obj['boundingBox']
        x0, y0, x1, y1 = bbox

        # Calculate the YOLO format values
        class_id = classes_to_ids.get(obj_type, 2)
        x_center = (x0 + x1) / 2.0 / image_width
        y_center = (y0 + y1) / 2.0 / image_height
        width = (x1 - x0) / image_width
        height = (y1 - y0) / image_height

        yolo_description.append(f"{class_id} {x_center} {y_center} {width} {height}")

    return "\n".join(yolo_description)
