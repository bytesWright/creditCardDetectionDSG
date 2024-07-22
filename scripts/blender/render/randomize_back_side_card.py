import bpy
from scripts.blender.spatial.compute_pixel_bounding_box import compute_vectors_pixel_bounding_box
from scripts.blender.images.assign_image_to_texture import assign_image_to_texture
from scripts.blender.material.update import randomize_material_parameters_from_template
from scripts.blender.spatial.compute_3d_bbox_positions import compute_3d_bbox_positions
from scripts.blender.render.spatial import randomize_card_position_and_rotation, calculate_center_and_plane_size
from scripts.templates.render_template import render_template


def randomize_back_side_card(root):
    file_path = f"{root}/assets/materials_randomization/Band.json"
    randomize_material_parameters_from_template(file_path)


def randomize_back_card(root, card_object):
    if isinstance(card_object, str):
        card_object = bpy.data.objects.get(card_object)

    randomize_card_position_and_rotation(card_object, side="back")
    bpy.context.view_layer.update()

    randomize_back_side_card(root)
    image, relative_bounding_boxes = render_template(
        root_path=root, width=900, height=540, side="back"
    )

    assign_image_to_texture("Back", "Color", image)
    center, size = calculate_center_and_plane_size(card_object)

    scene = bpy.context.scene
    camera = scene.camera  # Ensure the scene has a camera

    data = []

    for box in relative_bounding_boxes:
        bounding_box3d = compute_3d_bbox_positions(
            center,
            card_object.rotation_euler,
            size,
            box["relativeBoundingBox"],
            flip=True
        )

        data.append({
            "type": box["type"],
            "boundingBox3d": bounding_box3d,
            "boundingBox": compute_vectors_pixel_bounding_box(
                scene,
                bounding_box3d,
                camera
            )
        })

    return data


def randomize_card_back_plastic(root):
    file_path = f"{root}/assets/materials_randomization/Back.json"
    randomize_material_parameters_from_template(file_path)