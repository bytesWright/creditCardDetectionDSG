import json

import bpy

from .query import output_surface_node
from scripts.color.hsva_to_rgba import n_hsva_to_n_rgba
from scripts.blender.material.random_values import generate_random_value, identify_value


def update_parameter(material, node, input_name, new_value):
    node = node if node is not None else output_surface_node(material)

    if isinstance(node, str):
        node = material.node_tree.nodes[node]

    inpt = node.inputs[input_name]
    inpt.default_value = new_value

    for link in inpt.links:
        if link.is_valid:
            link.to_socket.default_value = new_value


def randomize_material_parameters(template):
    material_name = template.get("name")
    if not material_name:
        raise ValueError("No material name provided in the data.")

    material = bpy.data.materials.get(material_name)
    if material is None:
        raise ValueError(f"Material '{material_name}' not found.")

    material_nodes = material.node_tree.nodes

    for node_data in template["nodes"]:
        node_name = node_data["name"]
        inputs = node_data["inputs"]
        node = material_nodes[node_name]

        for input_data in inputs:
            input_name = input_data["name"]

            if "randomize" in input_data and input_data["randomize"]:
                default_value = input_data.get("defaultValue")
                value_type = input_data.get("inputType", None)
                sub_value_type = input_data.get("subType", None)

                try:
                    computed_value_type, computed_sub_value_type = identify_value(default_value)
                except:
                    raise Exception(f"Could not process default_value [{default_value}] of input [{input_name}] for material [{material_name}]")

                value_type = value_type if value_type is not None else computed_value_type
                sub_value_type = sub_value_type if sub_value_type is not None else computed_sub_value_type

                value_range = input_data.get("range")
                new_value = generate_random_value(value_type, sub_value_type, default_value=default_value, value_range=value_range)
            else:
                new_value = input_data.get("defaultValue")

            transform_instruction = input_data.get("transform")
            transformer = transformers.get(transform_instruction)

            if transformer is not None:
                new_value = transformer(new_value)

            update_parameter(material, node, input_name, new_value)


transformers = {
    "hsvaToRbga": n_hsva_to_n_rgba
}


def read_json_from_disk(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def randomize_material_parameters_from_template(filepath):
    data = read_json_from_disk(filepath)
    randomize_material_parameters(data)
