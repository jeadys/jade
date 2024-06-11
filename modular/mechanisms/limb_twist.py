import maya.cmds as cmds

from modular.biped.biped import Segment
from utilities.enums import MUDOperation


def calculate_distance_between(from_distance: str, to_distance: str) -> tuple[float, str]:
    distance_between_node: str = cmds.createNode("distanceBetween", name=f"{from_distance}_{to_distance}_distance_node")
    cmds.connectAttr(f"{from_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix1")
    cmds.connectAttr(f"{to_distance}.worldMatrix[0]", f"{distance_between_node}.inMatrix2")

    distance_between_value: float = cmds.getAttr(f"{distance_between_node}.distance")

    return distance_between_value, distance_between_node


class Twist:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def twist_joint(self, prefix, parent_segment: Segment, start_segment: Segment, end_segment: Segment, twist_amount,
                    twist_mechanic):
        distance_between_start_end, _ = calculate_distance_between(
            from_distance=f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT",
            to_distance=f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT")

        average_joint_position = distance_between_start_end / (twist_amount + 1)

        start_joint = cmds.joint(radius=3, name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_#")
        cmds.matchTransform(start_joint, f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT", position=True,
                            rotation=True, scale=False)

        end_joint = cmds.joint(radius=3, name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_end_#")
        cmds.matchTransform(end_joint, f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT", position=True,
                            rotation=True, scale=False)

        twist_handle = cmds.ikHandle(name=f"{prefix}{self.name}_{self.blueprint_nr}_twist_ikSCsolver_#",
                                     startJoint=start_joint, endEffector=end_joint, solver="ikSCsolver")[0]

        cmds.parent(twist_handle, f"{prefix}{parent_segment.name}_{self.blueprint_nr}_JNT")
        cmds.parent(start_joint, f"{prefix}{parent_segment.name}_{self.blueprint_nr}_JNT")

        if twist_mechanic == "upper":
            cmds.orientConstraint(f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT", end_joint,
                                  maintainOffset=False)
        elif twist_mechanic == "lower":
            cmds.orientConstraint(f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT", end_joint,
                                  maintainOffset=False)

        cmds.pointConstraint(f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT", twist_handle, maintainOffset=False)

        previous_joint = end_joint
        for x in range(twist_amount):
            cmds.select(deselect=True)
            between_joint = cmds.joint(name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_#")

            cmds.matchTransform(between_joint, end_joint, position=True, rotation=False, scale=False)
            cmds.matchTransform(between_joint, end_joint, position=False, rotation=True, scale=False)

            if twist_mechanic == "upper":
                cmds.move(0, -average_joint_position * (x + 1), 0, between_joint, relative=True, objectSpace=True)
            elif twist_mechanic == "lower":
                cmds.move(0, average_joint_position * (x + 1), 0, between_joint, relative=True, objectSpace=True)

            cmds.parent(between_joint, start_joint)

            divide = cmds.createNode("multiplyDivide", name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_DIVIDE_#")
            cmds.setAttr(f"{divide}.input2Y", 0.75)
            cmds.setAttr(f"{divide}.operation", MUDOperation.MULTIPLY.value)

            cmds.connectAttr(f"{previous_joint}.rotate.rotateY", f"{divide}.input1Y")
            cmds.connectAttr(f"{divide}.outputY", f"{between_joint}.rotate.rotateY")
            previous_joint = between_joint
