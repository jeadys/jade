from maya import cmds as cmds


def has_parent(from_parent, to_parent=None):
    current_parent = cmds.listRelatives(from_parent, parent=True)

    if to_parent is None:
        return current_parent is None

    return current_parent and current_parent[0] == to_parent
