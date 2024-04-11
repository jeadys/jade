import maya.cmds as cmds


def set_rgb_color(node: str, color: tuple[float, float, float]) -> None:
    transform_node_types = ["transform", "joint"]

    if cmds.nodeType(node) not in transform_node_types:
        raise ValueError(f"Node {node} is not a transform node")

    cmds.setAttr(f"{node}.overrideEnabled", True)
    cmds.setAttr(f"{node}.overrideRGBColors", True)
    cmds.setAttr(f"{node}.overrideColorRGB", *color)