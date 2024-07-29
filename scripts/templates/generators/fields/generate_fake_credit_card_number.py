import random


def luhn_checksum(card_number):
    """Calculate the Luhn checksum for a card number."""

    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def generate_luhn_valid_number(prefix, length):
    """Generate a Luhn-valid credit card number with the given prefix and length."""
    number = [int(x) for x in str(prefix)]
    while len(number) < (length - 1):
        number.append(random.randint(0, 9))
    checksum = luhn_checksum(int(''.join(map(str, number))) * 10)
    number.append((10 - checksum) % 10)
    return ''.join(map(str, number))


def insert_spaces(card_number):
    space_count = random.randint(1, 4)
    parts = [card_number[i:i + 4] for i in range(0, len(card_number), 4)]
    spaced_number = (' ' * space_count).join(parts)
    return spaced_number


def generate_fake_credit_card_number(card_type="VISA"):
    """Generate a fake credit card number for a given card type."""
    card_types = {
        "VISA": {"prefix": "4", "length": 16},
        "MASTERCARD": {"prefix": "51", "length": 16},
        "DISCOVER": {"prefix": "6011", "length": 16},
        "AMEX": {"prefix": "34", "length": 15},
    }

    if card_type not in card_types:
        raise ValueError(f"Unsupported card type: {card_type}")
    card_info = card_types[card_type]

    card_number = generate_luhn_valid_number(card_info["prefix"], card_info["length"])
    return insert_spaces(card_number)


def generate_random_credit_card_number():
    """Generate a fake credit card number with a randomly selected card type."""
    card_types = ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]
    selected_card_type = random.choice(card_types)
    return selected_card_type, generate_fake_credit_card_number(selected_card_type)
