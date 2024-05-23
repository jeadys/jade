import maya.cmds as cmds

from utilities.set_rgb_color import set_rgb_color


def create_curve_from_locators(points: list[list[float, float, float]], locators: list[str]):
    curve: str = cmds.curve(name=f"curve#", point=points, degree=1)
    shape_curve: str = cmds.listRelatives(curve, shapes=True, children=True)[0]
    set_rgb_color(node=curve, color=(1, 1, 1))

    for index, locator in enumerate(locators):
        shape_locator = cmds.listRelatives(locator, shapes=True, children=True)[0]
        # bake_transform_to_offset_parent_matrix(locator)
        cmds.connectAttr(f"{shape_locator}.worldPosition[0]", f"{shape_curve}.controlPoints[{index}]")


def create_visual_connection(from_node, to_node):
    # cmds.group(empty=True, name="curves")
    from_position = cmds.xform(from_node, query=True, translation=True, worldSpace=True)
    to_position = cmds.xform(to_node, query=True, translation=True, worldSpace=True)

    curve: str = cmds.curve(name=f"curve#", point=[from_position, to_position], degree=1)
    set_rgb_color(node=curve, color=(1, 0, 1))
    # cmds.parent(curve, group)

    shape_curve: str = cmds.listRelatives(curve, shapes=True, children=True)[0]
    from_shape = cmds.listRelatives(from_node, shapes=True, children=True)[0]
    to_shape = cmds.listRelatives(to_node, shapes=True, children=True)[0]

    cmds.connectAttr(f"{from_shape}.worldPosition[0]", f"{shape_curve}.controlPoints[0]")
    cmds.connectAttr(f"{to_shape}.worldPosition[0]", f"{shape_curve}.controlPoints[1]")

    cmds.move(*from_position, f"{curve}.scalePivot", f"{curve}.rotatePivot", absolute=True)