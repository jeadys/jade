import maya.cmds as cmds
import mechanisms.arm_stretch as arm_stretch_module
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape
from utilities.enums import RotateOrder
from dataclasses import dataclass

reload(control_shape)
reload(arm_stretch_module)


@dataclass(frozen=True)
class ArmSegment:
    name: str
    shape: str


class IKArm:
    def __init__(self, prefix) -> None:
        self.prefix = prefix
        self.arm_segments = (
            ArmSegment(name="upperarm", shape="circle"),
            ArmSegment(name="lowerarm", shape="circle"),
            ArmSegment(name="wrist", shape="star"),
        )

        self.kinematic_parent_group = f"{self.prefix}_arm_kinematics"
        self.control_parent_group = f"{self.prefix}_arm_controls"
        self.control_shape: ControlShape = ControlShape()

    def create_ik_arm_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_ik_joint = self.kinematic_parent_group
        for count, joint in enumerate(self.arm_segments):
            current_ik_joint = cmds.duplicate(f"{self.prefix}_DEF_{joint.name}", parentOnly=True, name=f"{self.prefix}_IK_{joint.name}")[0]
            cmds.parentConstraint(f"{self.prefix}_IK_{joint.name}", f"{self.prefix}_DEF_{joint.name}", maintainOffset=True)
            cmds.parent(current_ik_joint, previous_ik_joint)

            bake_transform_to_offset_parent_matrix(current_ik_joint)

            previous_ik_joint = current_ik_joint

    def create_ik_arm_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        ik_arm_ctrl = self.control_shape.select_control_shape(shape="circle", name=f"{self.prefix}_IK_CTRL_arm")
        cmds.setAttr(f"{ik_arm_ctrl}.rotateOrder", RotateOrder.ZXY.value)

        ik_elbow_ctrl = self.control_shape.select_control_shape(shape="star", name=f"{self.prefix}_IK_CTRL_elbow")
        cmds.setAttr(f"{ik_elbow_ctrl}.rotateOrder", RotateOrder.ZXY.value)

        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_arm",
            startJoint=f"{self.prefix}_IK_upperarm",
            endEffector=f"{self.prefix}_IK_wrist",
            solver="ikRPsolver")[0]

        # WRIST
        cmds.matchTransform(ik_arm_ctrl, f"{self.prefix}_IK_wrist", position=True, rotation=True,scale=False)
        cmds.parent(ik_handle, ik_arm_ctrl)
        cmds.orientConstraint(ik_arm_ctrl, f"{self.prefix}_IK_wrist", maintainOffset=True)
        cmds.parent(ik_arm_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_arm_ctrl)

        # POLE
        cmds.matchTransform(ik_elbow_ctrl, f"{self.prefix}_IK_lowerarm", position=True, rotation=False, scale=False)
        cmds.rotate(90, 0, 0, ik_elbow_ctrl, relative=True)
        position = cmds.xform(ik_elbow_ctrl, query=True, translation=True, worldSpace=True)
        cmds.move(position[0], position[1], position[2] - 75, ik_elbow_ctrl)
        cmds.poleVectorConstraint(ik_elbow_ctrl, ik_handle)
        cmds.parent(ik_elbow_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_elbow_ctrl)

    def create_elbow_space_swap(self):
        cmds.addAttr(
            f"{self.prefix}_IK_CTRL_elbow", attributeType="enum", enumName=f"WORLD=0:HAND=1", niceName="ELBOW_FOLLOW",
            longName="ELBOW_FOLLOW", defaultValue=0, keyable=True
        )

        elbow_space_swap = cmds.createNode("blendMatrix", name=f"{self.prefix}_blend_matrix_elbow_space_swap")
        offset_matrix = cmds.getAttr(f"{self.prefix}_IK_CTRL_elbow.offsetParentMatrix")
        cmds.setAttr(f"{elbow_space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_arm_swap_position = cmds.spaceLocator(name=f"{self.prefix}_ik_arm_swap_position")
        cmds.matchTransform(ik_arm_swap_position, f"{self.prefix}_IK_CTRL_elbow", position=True, rotation=True, scale=False)
        cmds.parent(ik_arm_swap_position, f"{self.prefix}_IK_CTRL_arm")

        bake_transform_to_offset_parent_matrix(ik_arm_swap_position[0])

        cmds.connectAttr(f"{ik_arm_swap_position[0]}.worldMatrix[0]", f"{elbow_space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{elbow_space_swap}.outputMatrix", f"{self.prefix}_IK_CTRL_elbow.offsetParentMatrix")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_elbow.ELBOW_FOLLOW", f"{elbow_space_swap}.envelope")

        cmds.addAttr(f"{self.prefix}_IK_CTRL_arm", longName="ELBOW_FOLLOW", proxy=f"{self.prefix}_IK_CTRL_elbow.ELBOW_FOLLOW")