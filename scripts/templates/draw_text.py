def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def clamp_normalized(value):
    return clamp(value, 0, 1)


def draw_left_justified_text(draw, image_size, position, text, font, color=(0, 0, 0), draw_rectangle=False):
    width, height = image_size

    draw.text(position, text, font=font, fill=color)
    bbox = draw.textbbox(position, text, font=font)

    x0, y0, x1, y1 = bbox

    if draw_rectangle:
        draw.rectangle([(x0, y0), (x1, y1)])

    x0_rel = x0 / width
    y0_rel = y0 / height
    x1_rel = x1 / width
    y1_rel = y1 / height

    return tuple(
        map(clamp_normalized, (x0_rel, y0_rel, x1_rel, y1_rel))
    )


def draw_right_justified_text(draw, image_size, position, text, font, color=(0, 0, 0), draw_rectangle=False):
    image_width, image_height = image_size

    lines = text.split('\n')
    line_widths = [draw.textlength(line, font=font) for line in lines]

    x0, y0 = float('inf'), float('inf')
    x1, y1 = float('-inf'), float('-inf')

    # Draw each line of text right justified
    for i, line in enumerate(lines):
        line_width = line_widths[i]
        x = position[0] - line_width
        y = position[1] + i * font.size

        # Update the bounding box
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, position[0])
        y1 = max(y1, y + font.size)

        draw.text((x, y), line, font=font, fill=color)

    if draw_rectangle:
        draw.rectangle([(x0, y0), (x1, y1)])

    # Normalize the bounding box coordinates
    x0_rel = x0 / image_width
    y0_rel = y0 / image_height
    x1_rel = x1 / image_width
    y1_rel = y1 / image_height

    return tuple(
        map(clamp_normalized, (x0_rel, y0_rel, x1_rel, y1_rel))
    )
