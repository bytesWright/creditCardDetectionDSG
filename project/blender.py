import os
import sys

import bpy


def include_blender_file_path():
    root = os.path.dirname(bpy.data.filepath)
    if root not in sys.path:
        sys.path.append(root)

    return root
