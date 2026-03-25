import os
import random

import bmesh
import bpy
import mathutils
from PIL import Image
from lambdawalker.blender.find_materials import find_materials_by_regex
from lambdawalker.blender.images.assign_image_to_texture import assign_image_to_texture
from lambdawalker.blender.material.randomize import randomize_material
from lambdawalker.blender.material.update import set_material_to_mesh
from lambdawalker.blender.query.get_scene_and_camera import get_scene_and_camera
from lambdawalker.blender.render.render_scene import render_scene
from lambdawalker.blender.spatial.compute_pixel_bounding_box import compute_obj_pixel_bounding_box, compute_vectors_pixel_bounding_box
from lambdawalker.file.path.ensure_directory import ensure_directory_for_file
from lambdawalker.yolo.log.vis_log import save_visual_log
from lambdawalker.yolo.log.yolo_log import create_yolo_description
from mathutils import Vector

from scripts.randomizer import randomize_environment, randomize_card_position_and_rotation


def render_id_simple_card(bucket_name, global_index: int, output_path: str, plain_id_ds, photo_id_ds, background_ds, classes):
    to_clean = []
    scene, camera = get_scene_and_camera()

    next_output_file = f"{output_path}/images/{bucket_name}/{global_index + 1}.jpg"
    output_file = f"{output_path}/images/{bucket_name}/{global_index}.jpg"

    if os.path.exists(next_output_file) and os.path.exists(output_file):
        return

    card_object_name = "card"
    card_object = bpy.data.objects.get(card_object_name)
    record = plain_id_ds[global_index]

    areas = record.objects

    objects_info = areas[0]
    card_object_class = objects_info["class"]

    randomize_card_position_and_rotation(
        card_object, object_class=card_object_class
    )

    id_card_image_pil, photo_image_pil = _prepare_card_images(record, photo_id_ds, objects_info)
    to_clean.append(id_card_image_pil)

    id_card_image_blender, hologram_image_blender = _setup_card_material(
        card_object_name, objects_info, id_card_image_pil, photo_image_pil
    )
    to_clean.extend([id_card_image_blender, hologram_image_blender])

    background_image_pil = _setup_background(global_index, background_ds)
    to_clean.append(background_image_pil)

    to_clean = to_clean + randomize_environment(background_image_pil)

    ensure_directory_for_file(output_file)
    render_scene(output_file)

    pos, rot, width, height = get_object_transform(card_object_name)
    percentual_coords = normalize_to_percentual(areas)

    coords = get_world_coordinates(pos, rot, width, height, percentual_coords, card_object_class)

    screen_bboxes = compute_screen_bounding_boxes(coords, scene, camera)

    bounding_box_data = [
        {"class": areas[i + 1]["class"], "boundingBox": bbb}
        for (i, bbb) in enumerate(screen_bboxes)
    ]

    _cleanup_blender_resources(to_clean)

    card_bounding_box = compute_obj_pixel_bounding_box(scene, card_object, camera)

    bounding_box_data += [
        {"class": card_object_class, "boundingBox": card_bounding_box}
    ]

    _save_yolo_annotations(
        output_path,
        bucket_name,
        global_index,
        scene,
        bounding_box_data,
        classes
    )

    _save_visualization(
        output_path,
        bucket_name,
        global_index,
        output_file,
        bounding_box_data
    )


def _prepare_card_images(record, photo_id_ds, objects_info):
    id_card_image_pil = record.image.to_pil()
    photo_id = objects_info["photo_id"]
    photo_record = photo_id_ds[photo_id]
    photo_image_pil = photo_record.image.to_pil()

    if objects_info["class"] == "vertical_card":
        id_card_image_pil = id_card_image_pil.rotate(-90, expand=1)
        photo_image_pil = photo_image_pil.rotate(-90, expand=1)

    return id_card_image_pil, photo_image_pil


def _setup_card_material(card_object_name, objects_info, id_card_image_pil, photo_image_pil):
    subtype = objects_info["subtype"]
    possible_materials = find_materials_by_regex(f"{subtype}.*") + find_materials_by_regex("df.*")
    material = random.choice(possible_materials)
    set_material_to_mesh(card_object_name, material)

    id_card_image_blender = assign_image_to_texture(material, "color_img", id_card_image_pil)
    hologram_image_blender = assign_image_to_texture(material, "hologram_img", photo_image_pil)

    randomize_material(material, random.randint(0, 99999999999))
    return id_card_image_blender, hologram_image_blender


def _setup_background(global_index, background_ds):
    mod_index = global_index % len(background_ds)
    print(f"Using background {mod_index}")
    return background_ds[mod_index].image.to_pil()


def _save_visualization(output_path, bucket_name, global_index, output_file, bounding_box_data):
    output_file_vis = f"{output_path}/vis/{bucket_name}/{global_index}.jpg"
    ensure_directory_for_file(output_file_vis)
    save_visual_log(output_file, bounding_box_data, output_file_vis)


def _cleanup_blender_resources(to_clean):
    for data in to_clean:
        if data is None:
            continue
        elif isinstance(data, Image.Image):
            data.close()
        elif isinstance(data, bpy.types.Image):
            data.buffers_free()
            bpy.data.images.remove(data, do_unlink=True)

    bpy.context.view_layer.update()
    bpy.data.orphans_purge(do_recursive=True)


def _save_yolo_annotations(output_path, bucket_name, global_index, scene, bounding_box_data, classes):
    render = scene.render
    render_scale = render.resolution_percentage / 100.0
    width, height = (render.resolution_x * render_scale, render.resolution_y * render_scale)

    yolo_data = create_yolo_description(
        bounding_box_data,
        width, height,
        classes
    )

    yolo_txt_path = f"{output_path}/labels/{bucket_name}/{global_index}.txt"
    ensure_directory_for_file(yolo_txt_path)

    with open(yolo_txt_path, 'w') as yolo_file:
        yolo_file.write(yolo_data)


def get_world_coordinates(pos, rot_euler, width, height, percent_areas, object_class):
    # 1. Setup Matrices
    translation_mat = mathutils.Matrix.Translation(pos)
    rotation_mat = mathutils.Euler(rot_euler, 'XYZ').to_matrix().to_4x4()
    scale_mat = mathutils.Matrix.Scale(1, 4)  # Assuming scale is applied via width/height

    world_mat = translation_mat @ rotation_mat

    results = []

    for area in percent_areas:
        px1, py1, px2, py2 = area
        factor = 1
        if object_class == "vertical_card":
            py1, px1, py2, px2 = area
            factor = -1

        # Corners in 0-1 range mapped to local metric space
        # We use Vector((x, y, 0)) to represent a point on the local plane
        local_corners = [
            mathutils.Vector(((px1 - 0.5) * width * factor, - (py1 - 0.5) * height, 0)),
            mathutils.Vector(((px2 - 0.5) * width * factor, - (py1 - 0.5) * height, 0)),
            mathutils.Vector(((px2 - 0.5) * width * factor, - (py2 - 0.5) * height, 0)),
            mathutils.Vector(((px1 - 0.5) * width * factor, - (py2 - 0.5) * height, 0))
        ]

        # 2. Transform each local vector to World Space
        # world_mat @ vector creates the 3D position
        world_corners = [(world_mat @ v).to_tuple() for v in local_corners]
        results.append(world_corners)

    return results


def normalize_to_percentual(data):
    """
    Takes a list of dicts.
    Uses the first element's boundingBox as the (W, H) reference.
    Returns a list of [x1, y1, x2, y2] in 0.0-1.0 range.
    """
    # 1. Get reference dimensions from the first entry
    # Expecting [min_x, min_y, max_x, max_y] or [0, 0, width, height]
    ref_box = data[0]["boundingBox"]
    ref_w = ref_box[2] - ref_box[0]
    ref_h = ref_box[3] - ref_box[1]

    percentual_results = []

    # 2. Iterate through the rest of the entries (skipping the first one)
    for entry in data[1:]:
        if "bbox" in entry:
            bbox = entry["bbox"]

            # Normalize coordinates
            # Formula: (value - offset) / total_dimension
            px1 = (bbox[0] - ref_box[0]) / ref_w
            py1 = (bbox[1] - ref_box[1]) / ref_h
            px2 = (bbox[2] - ref_box[0]) / ref_w
            py2 = (bbox[3] - ref_box[1]) / ref_h

            percentual_results.append([px1, py1, px2, py2])

    return percentual_results


def get_object_transform(obj_name):
    """
    Returns the world-space position and rotation (Euler) of an object.

    Args:
        obj_name (str): The name of the object in the Blender scene.

    Returns:
        tuple: (position_tuple, rotation_euler_tuple)
    """
    # Access the object by name
    obj = bpy.data.objects.get(obj_name)

    if obj is None:
        print(f"Error: Object '{obj_name}' not found.")
        return None

    # Get the World Matrix (this accounts for parent-child offsets)
    world_matrix = obj.matrix_world

    # Decompose the matrix into translation, rotation, and scale
    pos, rot_quat, scale = world_matrix.decompose()

    # Convert Quaternion to Euler (Radians)
    # Using 'XYZ' order as it is the Blender default
    rot_euler = rot_quat.to_euler('XYZ')
    dims = obj.dimensions

    return tuple(pos), tuple(rot_euler), dims.x, dims.y


def compute_screen_bounding_boxes(areas_in_space, scene, camera):
    return [compute_vectors_pixel_bounding_box(scene, a, camera) for a in areas_in_space]
