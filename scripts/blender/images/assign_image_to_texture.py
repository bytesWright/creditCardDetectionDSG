import bpy

from .image_type_conversion import create_blender_image


def assign_image_to_texture(material_name, node_name, image):
    if material_name not in bpy.data.materials:
        print(f"Material '{material_name}' not found.")
        return

    material = bpy.data.materials[material_name]

    # Ensure the material uses nodes
    if not material.use_nodes:
        print(f"Material '{material_name}' does not use nodes.")
        return

    nodes = material.node_tree.nodes

    # Check if the node exists
    if node_name not in nodes:
        print(f"Node '{node_name}' not found in material '{material_name}'.")
        return

    node = nodes[node_name]

    # Check if the node is an image texture node
    if node.type != 'TEX_IMAGE':
        print(f"Node '{node_name}' is not an image texture node.")
        return

    image = create_blender_image(image)

    # Assign the image to the node
    node.image = image
