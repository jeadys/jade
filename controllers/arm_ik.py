import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import RotateOrder

reload(control_shape)


# @dataclass(frozen=True)
# class ArmSegment:
#     name: str
#     shape: str
#

class ArmIK:
    def __init__(self, prefix, rotation_order) -> None:
        self.prefix = prefix
        self.rotation_order = rotation_order.upper()
        self.arm_segments = [f"{self.prefix}_clavicle", f"{self.prefix}_upperarm", f"{self.prefix}_lowerarm", f"{self.prefix}_wrist"]
        self.kinematic_parent_group = f"{self.prefix}_arm_kinematics"
        self.control_parent_group = f"{self.prefix}_arm_controls"
        self.control_shape: Curve = Curve()

    def create_arm_ik(self):
        self.create_ik_arm_joints()
        self.create_ik_arm_controls()
        self.create_elbow_space_swap()

    def create_ik_arm_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_ik_joint = self.kinematic_parent_group
        for count, joint in enumerate(self.arm_segments[1:]):
            current_ik_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_IK")[0]
            cmds.parentConstraint(current_ik_joint, joint, maintainOffset=True)
            cmds.parent(current_ik_joint, previous_ik_joint)

            bake_transform_to_offset_parent_matrix(current_ik_joint)

            previous_ik_joint = current_ik_joint

    def create_ik_arm_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        ik_arm_ctrl = self.control_shape.curve_four_way_arrow(name=f"{self.prefix}_arm_IK_CTRL")
        cmds.setAttr(f"{ik_arm_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)

        ik_elbow_ctrl = self.control_shape.curve_triangle(name=f"{self.prefix}_elbow_IK_CTRL")
        cmds.setAttr(f"{ik_elbow_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)

        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_arm",
            startJoint=f"{self.arm_segments[1]}_IK",
            endEffector=f"{self.arm_segments[-1]}_IK",
            solver="ikRPsolver")[0]

        # WRIST
        cmds.matchTransform(ik_arm_ctrl, f"{self.arm_segments[-1]}_IK", position=True, rotation=True, scale=False)
        cmds.parent(ik_handle, ik_arm_ctrl)
        cmds.orientConstraint(ik_arm_ctrl, f"{self.arm_segments[-1]}_IK", maintainOffset=True)
        cmds.parent(ik_arm_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_arm_ctrl)

        # POLE
        cmds.matchTransform(ik_elbow_ctrl, f"{self.arm_segments[1]}_IK", position=True, rotation=False, scale=False)
        cmds.rotate(90, 0, 0, ik_elbow_ctrl, relative=True)
        position = cmds.xform(ik_elbow_ctrl, query=True, translation=True, worldSpace=True)
        cmds.move(position[0], position[1], position[2] - 75, ik_elbow_ctrl)
        cmds.poleVectorConstraint(ik_elbow_ctrl, ik_handle)
        cmds.parent(ik_elbow_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_elbow_ctrl)

    def create_elbow_space_swap(self):

        cmds.addAttr(f"{self.prefix}_elbow_IK_CTRL", attributeType="enum", enumName=f"WORLD=0:HAND=1", niceName="ELBOW_FOLLOW",
                     longName="ELBOW_FOLLOW", defaultValue=0, keyable=True)

        elbow_space_swap = cmds.createNode("blendMatrix", name=f"{self.prefix}_blend_matrix_elbow_space_swap")
        offset_matrix = cmds.getAttr(f"{self.prefix}_elbow_IK_CTRL.offsetParentMatrix")
        cmds.setAttr(f"{elbow_space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_arm_swap_position = cmds.spaceLocator(name=f"{self.prefix}_ik_arm_swap_position")
        cmds.matchTransform(ik_arm_swap_position, f"{self.prefix}_elbow_IK_CTRL", position=True, rotation=True, scale=False)
        cmds.parent(ik_arm_swap_position, f"{self.prefix}_arm_IK_CTRL")

        bake_transform_to_offset_parent_matrix(ik_arm_swap_position[0])

        cmds.connectAttr(f"{ik_arm_swap_position[0]}.worldMatrix[0]", f"{elbow_space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{elbow_space_swap}.outputMatrix", f"{self.prefix}_elbow_IK_CTRL.offsetParentMatrix")
        cmds.connectAttr(f"{self.prefix}_elbow_IK_CTRL.ELBOW_FOLLOW", f"{elbow_space_swap}.envelope")

        cmds.addAttr(f"{self.prefix}_arm_IK_CTRL", longName="ELBOW_FOLLOW", proxy=f"{self.prefix}_elbow_IK_CTRL.ELBOW_FOLLOW")
