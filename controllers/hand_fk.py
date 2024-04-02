import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import RotateOrder

reload(control_shape)


class HandFK:

    def __init__(self, prefix, rotation_order) -> None:
        self.prefix = prefix
        self.rotation_order = rotation_order.upper()
        self.hand_segments = [f"{self.prefix}_thumb", f"{self.prefix}_index", f"{self.prefix}_middle", f"{self.prefix}_ring", f"{self.prefix}_pinky"]
        self.control_parent_group = f"{self.prefix}_arm_controls"
        self.control_shape: Curve = Curve()

    def create_hand_fk(self):
        self.create_fk_hand_controls()

    def create_fk_hand_controls(self) -> None:
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        hand = cmds.group(empty=True, name="hand")
        cmds.parent(hand, self.control_parent_group)
        cmds.matchTransform(hand, f"{self.prefix}_wrist", position=True, rotation=True, scale=False)
        for index, joint in enumerate(self.hand_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_fk_ctrl = self.control_shape.curve_cube(name=f"{joint}_FK_CTRL")
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)
            cmds.matchTransform(current_fk_ctrl, joint, position=True, rotation=True, scale=False)

            cmds.parent(current_fk_ctrl, hand)
            cmds.parentConstraint(current_fk_ctrl, joint, maintainOffset=False)

            bake_transform_to_offset_parent_matrix(current_fk_ctrl)
            cmds.parentConstraint(f"{self.prefix}_wrist", hand, maintainOffset=True)

            previous_fk_ctrl = current_fk_ctrl

            children = cmds.listRelatives(joint, allDescendents=True, shapes=False, type="joint")
            children.reverse()
            for sub_index, sub_joint in enumerate(children[:-1]):
                current_sub_fk_ctrl = self.control_shape.curve_cube(name=f"{sub_joint}_FK_CTRL")
                cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)
                cmds.matchTransform(current_sub_fk_ctrl, sub_joint, position=True, rotation=True, scale=False)
                cmds.parent(current_sub_fk_ctrl, previous_fk_ctrl)
                cmds.parentConstraint(current_sub_fk_ctrl, sub_joint, maintainOffset=False)

                bake_transform_to_offset_parent_matrix(current_sub_fk_ctrl)

                previous_fk_ctrl = current_sub_fk_ctrl
