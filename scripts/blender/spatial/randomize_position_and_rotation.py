import random
from mathutils import Vector, Euler
from scripts.blender.spatial.parce_distance import parse_distance


def randomize_position_and_rotation(obj, pos_range, rot_range, point=("0m", "0m", "0m"), rotation=(0, 0, 0)):
    # Parse position range
    pos_x_range = parse_distance(pos_range[0])
    pos_y_range = parse_distance(pos_range[1])
    pos_z_range = parse_distance(pos_range[2])

    # Generate random position within range and add to the point
    pos_x = parse_distance(point[0]) + random.uniform(-pos_x_range, pos_x_range)
    pos_y = parse_distance(point[1]) + random.uniform(-pos_y_range, pos_y_range)
    pos_z = parse_distance(point[2]) + random.uniform(-pos_z_range, pos_z_range)

    # Apply random position
    obj.location = Vector((pos_x, pos_y, pos_z))

    # Generate random rotation within range (radians)
    rot_x = random.uniform(-rot_range[0], rot_range[0]) + rotation[0]
    rot_y = random.uniform(-rot_range[1], rot_range[1]) + rotation[1]
    rot_z = random.uniform(-rot_range[2], rot_range[2]) + rotation[2]

    # Apply random rotation
    obj.rotation_euler = Euler((rot_x, rot_y, rot_z), 'XYZ')