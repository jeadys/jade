import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import RotateOrder

reload(control_shape)


class LegFK:
    def __init__(self, prefix, rotation_order) -> None:
        self.prefix = prefix
        self.rotation_order = rotation_order.upper()
        self.leg_segments = [f"{self.prefix}_upperleg", f"{self.prefix}_lowerleg", f"{self.prefix}_ankle", f"{self.prefix}_ball", f"{self.prefix}_toe"]
        self.control_parent_group = f"{self.prefix}_leg_controls"
        self.kinematic_parent_group = f"{self.prefix}_leg_kinematics"
        self.control_shape: Curve = Curve()

    def create_leg_fk(self):
        self.create_leg_fk_joints()
        self.create_leg_fk_controls()

    def create_leg_fk_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_fk_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.leg_segments):
            current_fk_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_FK")[0]
            cmds.parentConstraint(current_fk_joint, joint, maintainOffset=True)
            cmds.parent(current_fk_joint, previous_fk_joint)

            bake_transform_to_offset_parent_matrix(current_fk_joint)

            previous_fk_joint = current_fk_joint

    def create_leg_fk_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        previous_fk_control = self.control_parent_group
        for index, joint in enumerate(self.leg_segments[:-1]):
            current_fk_ctrl = self.control_shape.curve_circle(name=f"{joint}_FK_CTRL")
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)
            cmds.matchTransform(current_fk_ctrl, joint, position=True, rotation=True, scale=False)
            cmds.parent(current_fk_ctrl, previous_fk_control)

            bake_transform_to_offset_parent_matrix(current_fk_ctrl)

            if index == 0:
                cmds.connectAttr(f"{joint}_FK_CTRL.worldMatrix[0]",
                                 f"{joint}_FK.offsetParentMatrix")
            else:
                cmds.connectAttr(f"{joint}_FK_CTRL.translate", f"{joint}_FK.translate")
                cmds.connectAttr(f"{joint}_FK_CTRL.rotate", f"{joint}_FK.rotate")

            previous_fk_control = current_fk_ctrl


if __name__ == "__main__":
    pass
