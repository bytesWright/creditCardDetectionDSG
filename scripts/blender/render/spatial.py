import math
import mathutils

from scripts.blender.spatial.randomize_position_and_rotation import randomize_position_and_rotation


def randomize_card_position_and_rotation(card_object, side="front"):
    position_range = ("5mm", "5mm", "2.5mm")
    point = ("0mm", "0mm", "6.5mm")

    rotation = (0, math.radians(180) if side == "back" else 0, 0)
    rotation_range = list(map(math.radians, (3, 3, 1.5)))
    randomize_position_and_rotation(card_object, position_range, rotation_range, point, rotation)


def calculate_center_and_plane_size(obj):
    return tuple(obj.matrix_world @ mathutils.Vector((0, 0, .0005))), obj.dimensions[:2]