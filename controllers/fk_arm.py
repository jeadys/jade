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


class FKArm:
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

    def create_fk_arm_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_fk_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.arm_segments):
            current_fk_joint = cmds.duplicate(f"{self.prefix}_DEF_{joint.name}", parentOnly=True, name=f"{self.prefix}_FK_{joint.name}")[0]
            cmds.parentConstraint(f"{self.prefix}_FK_{joint.name}", f"{self.prefix}_DEF_{joint.name}", maintainOffset=True)
            cmds.parent(current_fk_joint, previous_fk_joint)

            bake_transform_to_offset_parent_matrix(current_fk_joint)

            previous_fk_joint = current_fk_joint

    def create_fk_arm_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        previous_fk_control = self.control_parent_group
        for index, joint in enumerate(self.arm_segments):
            current_fk_ctrl = self.control_shape.select_control_shape(shape=joint.shape, name=f"{self.prefix}_FK_CTRL_{joint.name}")
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder.ZXY.value)
            cmds.matchTransform(current_fk_ctrl, f"{self.prefix}_DEF_{joint.name}", position=True, rotation=True, scale=False)
            cmds.parent(current_fk_ctrl, previous_fk_control)

            if index == 0:
                cmds.connectAttr(f"{self.prefix}_FK_CTRL_{joint.name}.worldMatrix[0]",
                                 f"{self.prefix}_FK_{joint.name}.offsetParentMatrix")
            else:
                cmds.connectAttr(f"{self.prefix}_FK_CTRL_{joint.name}.translate", f"{self.prefix}_FK_{joint.name}.translate")
                cmds.connectAttr(f"{self.prefix}_FK_CTRL_{joint.name}.rotate", f"{self.prefix}_FK_{joint.name}.rotate")

            bake_transform_to_offset_parent_matrix(current_fk_ctrl)

            previous_fk_control = current_fk_ctrl
