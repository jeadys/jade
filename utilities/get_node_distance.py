import maya.cmds as cmds


def calculate_distance_between(from_distance: str, to_distance: str) -> tuple[float, str]:
    distance_between_node: str = cmds.createNode("distanceBetween", name=f"{from_distance}_{to_distance}_distance_node")
    cmds.connectAttr(f"{from_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix1")
    cmds.connectAttr(f"{to_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix2")

    distance_between_value: float = cmds.getAttr(f"{distance_between_node}.distance")

    return distance_between_value, distance_between_node


def add_node_distances(self, distance_one, distance_two):
    add_distances_node = cmds.createNode("addDoubleLinear", name=f"{self.prefix}_limb_length")

    cmds.connectAttr(f"{distance_one}.distance", f"{add_distances_node}.input1")
    cmds.connectAttr(f"{distance_two}.distance", f"{add_distances_node}.input2")
