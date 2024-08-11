import maya.cmds as cmds


def set_rgb_color(transform: str, rgb: tuple[float, float, float]) -> None:
    transform_node_types = ["transform", "joint"]

    if cmds.nodeType(transform) not in transform_node_types:
        return cmds.warning(f"{transform} is not a transform node")

    cmds.setAttr(f"{transform}.overrideEnabled", True)
    cmds.setAttr(f"{transform}.overrideRGBColors", True)
    cmds.setAttr(f"{transform}.overrideColorRGB", *rgb)


def set_index_color(node: str, index: int) -> None:
    transform_node_types = ["transform", "joint"]

    if cmds.nodeType(node) not in transform_node_types:
        return cmds.warning(f"{node} is not a transform node")

    if not (0 <= index <= 31):
        return cmds.warning("Color index must be between 0 and 31")

    cmds.setAttr(f"{node}.overrideEnabled", True)
    cmds.setAttr(f"{node}.overrideColor", index)
