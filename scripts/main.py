import os

from scripts.blender.query.get_scene_and_camera import get_scene_and_camera
from scripts.blender.render.render_card_side import render_card_side, query_root_path


def render_front(root=None, output_path=None, bucket="train", index=0, scene=None, camera=None):
    render_card_side(root, output_path, bucket, index, scene, camera, 'front')


def render_back(root=None, output_path=None, bucket="train", index=0, scene=None, camera=None):
    render_card_side(root, output_path, bucket, index, scene, camera, 'back')


def render_bulk():
    root = query_root_path()
    scene, camera = get_scene_and_camera()

    data_set_name = "creditCardV0.3"

    distribution = [
        {"name": "train", "limit": 3000},
        {"name": "val", "limit": 1000},
        {"name": "test", "limit": 1000}
    ]

    for bucket in distribution:
        output_path = os.path.join(root, "output", data_set_name)

        for i in range(0, bucket["limit"]):
            if i % 2 == 0:
                render_front(root, output_path, bucket["name"], i, scene, camera)
            else:
                render_back(root, output_path, bucket["name"], i, scene, camera)
