from maya import cmds as cmds


def has_parent(from_parent, to_parent=None):
    current_parent = cmds.listRelatives(from_parent, parent=True)

    if to_parent is None:
        return current_parent is None

    return current_parent and current_parent[0] == to_parent


def singleton(class_instance):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]

    return get_instance()
