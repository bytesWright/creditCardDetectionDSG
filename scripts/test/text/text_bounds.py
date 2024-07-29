from PIL import Image, ImageDraw, ImageFont

from scripts.templates.draw_text import draw_right_justified_text


def assert_value_is_normalized(value, min_value=0, max_value=1):
    assert min_value <= value <= max_value, f"Value {value} is not within the range {min_value}-{max_value}"


def test_text_out_of_bound_on_bottom_left():
    image = Image.new("RGB", (400, 400), (255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(20.0)

    bounds = draw_right_justified_text(
        draw,
        image.size,
        (200, 360),
        "Very long text out of bounds of the image\n" * 3,
        font,
        (0, 0, 0)
    )

    image.show()

    assert_value_is_normalized(bounds[0])
    assert_value_is_normalized(bounds[1])
    assert_value_is_normalized(bounds[2])
    assert_value_is_normalized(bounds[3])


def test_text_out_of_bound_on_bottom_right():
    image = Image.new("RGB", (400, 400), (255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(20.0)

    bounds = draw_right_justified_text(
        draw,
        image.size,
        (450, 360),
        "Very long text out of bounds of the image\n" * 3,
        font,
        (0, 0, 0)
    )

    image.show()

    assert_value_is_normalized(bounds[0])
    assert_value_is_normalized(bounds[1])
    assert_value_is_normalized(bounds[2])
    assert_value_is_normalized(bounds[3])


def test_text_out_of_bound_on_the_left():
    image = Image.new("RGB", (400, 400), (255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(20.0)

    bounds = draw_right_justified_text(
        draw,
        image.size,
        (-10, 200),
        "Very long text out of bounds of the image\n" * 3,
        font,
        (0, 0, 0)
    )

    image.show()

    assert_value_is_normalized(bounds[0])
    assert_value_is_normalized(bounds[1])
    assert_value_is_normalized(bounds[2])
    assert_value_is_normalized(bounds[3])


def test_text_out_of_bound_on_the_top():
    image = Image.new("RGB", (400, 400), (255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(20.0)

    bounds = draw_right_justified_text(
        draw,
        image.size,
        (360, -200),
        "Very long text out of bounds of the image\n" * 3,
        font,
        (0, 0, 0)
    )

    image.show()

    assert_value_is_normalized(bounds[0])
    assert_value_is_normalized(bounds[1])
    assert_value_is_normalized(bounds[2])
    assert_value_is_normalized(bounds[3])
