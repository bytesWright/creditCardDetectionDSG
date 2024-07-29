import random


def get_random_member(dct: dict, force=None):
    options = tuple(dct.keys())
    choice = random.choice(options) if force is None else force
    return choice, dct[choice]
