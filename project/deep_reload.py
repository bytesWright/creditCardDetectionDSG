import importlib
import os
import sys
import types

# Dictionary to store last modified times of modules
from project.modules_time_table import last_modified_times


def get_module_file(module):
    if hasattr(module, '__file__') and module.__file__:
        return module.__file__
    return None


def module_was_modified(module):
    module_file = get_module_file(module)

    if not module_file:
        return False

    current_mod_time = os.path.getmtime(module_file)

    if module_file not in last_modified_times:
        last_modified_times[module_file] = current_mod_time
        return False

    if current_mod_time != last_modified_times[module_file]:
        last_modified_times[module_file] = current_mod_time
        return True

    return False


def module_was_deleted(module):
    module_file = get_module_file(module)

    if not module_file:
        return False

    return not os.path.exists(module_file)


def reload_module_and_children(module, mem=None, root=None):
    if mem is None:
        mem = set()

    if module.__name__ in mem:
        return module

    if module_was_deleted(module):
        return None

    modified = module_was_modified(module)

    if modified:
        print(f"Reloading {module.__name__}")
        module = importlib.reload(module)

    if root is None:
        root = os.path.dirname(module.__file__)
    elif not hasattr(module, "__file__") or not module.__file__.startswith(root):
        return module

    for attr_name in dir(module):
        member = getattr(module, attr_name)

        if isinstance(member, types.ModuleType):
            reloaded = reload_module_and_children(member, mem, root)

            if reloaded is None:
                print(f"Module {attr_name} is deleted")
                delattr(module, attr_name)
            else:
                setattr(module, attr_name, reloaded)

        if isinstance(member, types.FunctionType):
            member_module = sys.modules[member.__module__]

            if member_module is not module:
                reloaded = reload_module_and_children(member_module, mem, root)
                if reloaded is not None:
                    function = getattr(reloaded, member.__name__)
                    setattr(module, attr_name, function)
                else:
                    print(f"Function {attr_name} is deleted")
                    delattr(module, attr_name)

    return module
