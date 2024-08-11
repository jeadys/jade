import maya.cmds as cmds


def lock_node(node):
    if not cmds.objExists(node):
        return cmds.warning(f"{node} couldn't be locked")

    if cmds.lockNode(query=True, lock=False):
        return cmds.warning(f"{node} is already locked")

    cmds.lockNode(node, lock=True)


def unlock_node(node):
    if not cmds.objExists(node):
        return cmds.warning(f"{node} couldn't be unlocked")

    if cmds.lockNode(query=True, lock=True):
        return cmds.warning(f"{node} is already unlocked")

    cmds.lockNode(node, lock=False)


def calculate_distance_between(from_distance: str, to_distance: str, delete_node=True) -> float:
    distance_between_node: str = cmds.createNode("distanceBetween", name=f"{from_distance}_{to_distance}_distance")
    cmds.connectAttr(f"{from_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix1")
    cmds.connectAttr(f"{to_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix2")

    distance_between_value: float = cmds.getAttr(f"{distance_between_node}.distance")

    if delete_node:
        cmds.delete(distance_between_node)

    return distance_between_value


def add_double_linear(distance_one, distance_two, delete_node=True) -> float:
    double_linear_node = cmds.createNode("addDoubleLinear", name=f"{distance_two}_{distance_two}_linear")
    cmds.connectAttr(f"{distance_one}.distance", f"{double_linear_node}.input1")
    cmds.connectAttr(f"{distance_two}.distance", f"{double_linear_node}.input2")

    double_linear_value: float = cmds.getAttr(f"{double_linear_node}.output")

    if delete_node:
        cmds.delete(double_linear_node)

    return double_linear_value
