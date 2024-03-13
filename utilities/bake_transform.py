import maya.cmds as cmds


def bake_transform_to_offset_parent_matrix(node):
    transform_node_types = ["transform", "joint"]

    if cmds.nodeType(node) not in transform_node_types:
        raise ValueError(f"Node {node} is not a transform node")

    local_matrix = cmds.xform(node, q=True, matrix=True, ws=False)
    cmds.setAttr(node + ".offsetParentMatrix", local_matrix, type="matrix")

    reset_transforms(node)


def reset_transforms(node):
    for attribute in ["translate", "rotate", "scale", "jointOrient"]:
        value = 1 if attribute == "scale" else 0

        for axis in "XYZ":
            if cmds.attributeQuery(f"{attribute}{axis}", node=node, exists=True):
                attribute_name = f"{node}.{attribute}{axis}"

                if not cmds.getAttr(attribute_name, lock=True):
                    cmds.setAttr(attribute_name, value)