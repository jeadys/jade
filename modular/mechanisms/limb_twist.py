import maya.cmds as cmds

from modular.biped.biped import Segment
from utilities.enums import MUDOperation, TwistFlow, RotateOrder
from utilities.get_node_distance import calculate_distance_between


class Twist:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def twist_joint(self, prefix, parent_segment: Segment, start_segment: Segment, end_segment: Segment,
                    twist_flow: TwistFlow):

        joint_layer_group = f"{prefix}{self.name}_{self.blueprint_nr}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            cmds.group(empty=True, name=joint_layer_group)

        joint_group = f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_GROUP"
        if not cmds.objExists(joint_group):
            cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_GROUP")
            cmds.parent(joint_group, joint_layer_group)

        start_joint = cmds.duplicate(f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT",
                                     name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_{twist_flow}",
                                     parentOnly=True)[0]

        end_joint = cmds.duplicate(f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT",
                                   name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_end_{twist_flow}",
                                   parentOnly=True)[0]

        cmds.parent(start_joint, joint_group)
        cmds.parent(end_joint, start_joint)

        if twist_flow == TwistFlow.FORWARD:
            cmds.orientConstraint(f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT", end_joint,
                                  maintainOffset=True, skip=["x", "z"])
            cmds.orientConstraint(f"{prefix}{start_segment.name}_{self.blueprint_nr}_JNT", start_joint,
                                  maintainOffset=True, skip=["y"])
            cmds.pointConstraint(f"{prefix}{parent_segment.name}_{self.blueprint_nr}_JNT", start_joint,
                                 maintainOffset=True)
        elif twist_flow == TwistFlow.BACKWARD:
            cmds.orientConstraint(f"{prefix}{end_segment.name}_{self.blueprint_nr}_JNT", end_joint,
                                  maintainOffset=True)
            cmds.parentConstraint(f"{prefix}{parent_segment.name}_{self.blueprint_nr}_JNT", start_joint,
                                  maintainOffset=True)

        return start_joint, end_joint

    def setup_twist_hierarchy(self, prefix, start_joint, end_joint):
        mult_matrix = cmds.createNode("multMatrix", name=f"{prefix}{self.name}_{self.blueprint_nr}_multMatrix_#")
        decompose_matrix = cmds.createNode("decomposeMatrix",
                                           name=f"{prefix}{self.name}_{self.blueprint_nr}_decomposeMatrix_#")
        quat_to_euler = cmds.createNode("quatToEuler", name=f"{prefix}{self.name}_{self.blueprint_nr}_quatToEuler_#")
        cmds.setAttr(f"{quat_to_euler}.inputRotateOrder", 1)

        cmds.connectAttr(f"{end_joint}.worldMatrix[0]", f'{mult_matrix}.matrixIn[0]')
        cmds.connectAttr(f"{start_joint}.worldInverseMatrix[0]", f'{mult_matrix}.matrixIn[1]')

        cmds.connectAttr(f"{mult_matrix}.matrixSum", f'{decompose_matrix}.inputMatrix')
        cmds.connectAttr(f"{decompose_matrix}.outputQuatY", f'{quat_to_euler}.inputQuatY')
        cmds.connectAttr(f"{decompose_matrix}.outputQuatW", f'{quat_to_euler}.inputQuatW')

        twist_amount = cmds.getAttr(f"{self.node}.twist_joints")
        distance_between_start_end, _ = calculate_distance_between(from_distance=start_joint, to_distance=end_joint)
        average_joint_position = distance_between_start_end / (twist_amount + 1)

        previous_joint = None
        for x in range(twist_amount):
            cmds.select(deselect=True)
            between_joint = cmds.joint(name=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_#",
                                       rotationOrder=RotateOrder.YZX.name)

            cmds.matchTransform(between_joint, end_joint, position=True, rotation=False, scale=False)
            cmds.parent(between_joint, start_joint)
            cmds.joint(between_joint, edit=True, orientJoint="none", zeroScaleOrient=True)
            cmds.move(0, -average_joint_position * (x + 1), 0, between_joint, relative=True, objectSpace=True)

            multiply_divide = cmds.createNode("multiplyDivide",
                                              name=f"{prefix}{self.name}_{self.blueprint_nr}_multiplyDivide_#")
            cmds.connectAttr(f"{self.node}.twist_influence", f"{multiply_divide}.input2Y")
            cmds.setAttr(f"{multiply_divide}.operation", MUDOperation.MULTIPLY.value)

            if previous_joint:
                cmds.connectAttr(f"{previous_joint}.rotateY", f"{multiply_divide}.input1Y")
            else:
                cmds.connectAttr(f"{quat_to_euler}.outputRotateY", f'{multiply_divide}.input1Y')

            cmds.connectAttr(f"{multiply_divide}.outputY", f"{between_joint}.rotateY")

            previous_joint = between_joint
