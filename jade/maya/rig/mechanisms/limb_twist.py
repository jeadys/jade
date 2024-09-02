import maya.cmds as cmds

from jade.enums import MUDOperation, RotateOrder


class Twist:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"

    def twist_joint(self, segments, twist_amount):
        for i in range(len(segments) - 1):
            start_segment = segments[i]
            end_segment = segments[i + 1]

            joint_layer_group = f"{self.prefix}_LAYER_GROUP"
            if not cmds.objExists(joint_layer_group):
                cmds.group(empty=True, name=joint_layer_group)

            joint_group = f"{self.prefix}_TWIST_GROUP"
            if not cmds.objExists(joint_group):
                cmds.group(empty=True, name=f"{self.prefix}_TWIST_GROUP")
                cmds.parent(joint_group, joint_layer_group)

            start_joint = cmds.duplicate(f"{start_segment}_JNT",
                                         name=f"{self.prefix}_TWIST_start_#", parentOnly=True)[0]

            end_joint = cmds.duplicate(f"{end_segment}_JNT",
                                       name=f"{self.prefix}_TWIST_end_#", parentOnly=True)[0]

            cmds.parent(start_joint, joint_group)
            cmds.parent(end_joint, start_joint)

            if i == len(segments) - 2:
                cmds.orientConstraint(f"{end_segment}_JNT", end_joint, maintainOffset=True)
                cmds.parentConstraint(f"{start_segment}_JNT", start_joint, maintainOffset=True)
            else:
                cmds.orientConstraint(f"{start_segment}_JNT", end_joint, maintainOffset=True, skip=["y", "z"])
                cmds.orientConstraint(f"{start_segment}_JNT", start_joint, maintainOffset=True, skip=["x"])
                cmds.pointConstraint(f"{start_segment}_JNT", start_joint, maintainOffset=True)

            self.setup_twist_hierarchy(start_joint=start_joint, end_joint=end_joint, twist_amount=twist_amount)

    def setup_twist_hierarchy(self, start_joint, end_joint, twist_amount):
        mult_matrix = cmds.createNode("multMatrix", name=f"{self.prefix}_multMatrix_#")
        decompose_matrix = cmds.createNode("decomposeMatrix", name=f"{self.prefix}_decomposeMatrix_#")
        quat_to_euler = cmds.createNode("quatToEuler", name=f"{self.prefix}_quatToEuler_#")
        cmds.setAttr(f"{quat_to_euler}.inputRotateOrder", 1)

        cmds.connectAttr(f"{end_joint}.worldMatrix[0]", f'{mult_matrix}.matrixIn[0]')
        cmds.connectAttr(f"{start_joint}.worldInverseMatrix[0]", f'{mult_matrix}.matrixIn[1]')

        cmds.connectAttr(f"{mult_matrix}.matrixSum", f'{decompose_matrix}.inputMatrix')
        cmds.connectAttr(f"{decompose_matrix}.outputQuatX", f'{quat_to_euler}.inputQuatX')
        cmds.connectAttr(f"{decompose_matrix}.outputQuatW", f'{quat_to_euler}.inputQuatW')

        # distance_between_start_end, _ = calculate_distance_between(from_distance=start_joint, to_distance=end_joint)
        # average_joint_position = distance_between_start_end / (twist_amount + 1)

        previous_joint = None
        for j in range(1, twist_amount + 1):
            cmds.select(deselect=True)
            between_joint = cmds.joint(name=f"{self.prefix}_TWIST_#", rotationOrder=RotateOrder.XYZ.name)

            cmds.matchTransform(between_joint, start_joint, position=True, rotation=False, scale=False)
            cmds.parent(between_joint, start_joint)
            cmds.joint(between_joint, edit=True, orientJoint="none", zeroScaleOrient=True)
            # cmds.move(-average_joint_position * (j + 1), 0, 0, between_joint, relative=True, objectSpace=True)

            constraint = cmds.pointConstraint([end_joint, start_joint], between_joint, maintainOffset=False)[0]
            weight_b = j / (twist_amount + 1)
            weight_a = 1.0 - weight_b

            cmds.setAttr(f"{constraint}.{start_joint}W1", weight_b)
            cmds.setAttr(f"{constraint}.{end_joint}W0", weight_a)
            cmds.delete(constraint)

            multiply_divide = cmds.createNode("multiplyDivide", name=f"{self.prefix}_multiplyDivide_#")
            # cmds.connectAttr(f"{self.node}.twist_influence", f"{multiply_divide}.input2X")
            cmds.setAttr(f"{multiply_divide}.input2X", 0.5)
            cmds.setAttr(f"{multiply_divide}.operation", MUDOperation.MULTIPLY.value)

            if previous_joint:
                cmds.connectAttr(f"{previous_joint}.rotateX", f"{multiply_divide}.input1X")
            else:
                cmds.connectAttr(f"{quat_to_euler}.outputRotateX", f'{multiply_divide}.input1X')

            cmds.connectAttr(f"{multiply_divide}.outputX", f"{between_joint}.rotateX")

            previous_joint = between_joint
