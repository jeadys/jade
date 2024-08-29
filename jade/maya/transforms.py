import maya.cmds as cmds


def node_exists(func):
    def wrapper(node, *args, **kwargs):
        if not cmds.objExists(node):
            return cmds.warning(f"{node} doesn't exist")

        result = func(node, *args, **kwargs)
        return result

    return wrapper


@node_exists
def bake_transform_to_offset_parent_matrix(node):
    transform_node_types = ["transform", "joint"]

    if cmds.nodeType(node) not in transform_node_types:
        return cmds.warning(f"Node {node} is not a transform node")

    local_matrix = cmds.xform(node, q=True, matrix=True, ws=False)
    cmds.setAttr(node + ".offsetParentMatrix", local_matrix, type="matrix")

    reset_transforms(node)


@node_exists
def reset_transforms(node):
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        value = 1 if attribute == "scale" else 0

        for axis in "XYZ":
            if cmds.attributeQuery(f"{attribute}{axis}", node=node, exists=True):
                attribute_name = f"{node}.{attribute}{axis}"
                cmds.setAttr(attribute_name, value)


@node_exists
def hide_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, keyable=True, channelBox=True)


@node_exists
def unhide_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, keyable=False, channelBox=False)


@node_exists
def lock_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, lock=True)


@node_exists
def unlock_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, lock=False)


@node_exists
def lock_and_hide_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, lock=True, keyable=False, channelBox=False)


@node_exists
def unlock_and_unhide_transforms(node):
    for attribute in ["translate", "rotate", "scale"]:
        for axis in "XYZ":
            attribute_name = f"{node}.{attribute}{axis}"
            cmds.setAttr(attribute_name, lock=False, keyable=True, channelBox=True)
