import maya.cmds as cmds

from joints.joint_layer import create_layer_joints

from utilities.curve import Curve
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import RotateOrder


class FKChain:
    def __init__(self, prefix: str, name: str):
        self.prefix = prefix
        self.name = name
        self.kinematic_parent_group: str = f"{self.prefix}_{self.name}_kinematics"
        self.control_parent_group: str = f"{self.prefix}_{self.name}_controls"
        self.curve_instance: Curve = Curve()

    def create_fk_joints(self, segments: list[str]) -> list[str]:
        fk_joints: list[str] = create_layer_joints(prefix=self.prefix, name=self.name, layer_name="FK", segments=segments)

        return fk_joints

    def create_fk_controls(self, segments: list[str], rotation_order: str, scale: float) -> list[str]:
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        fk_ctrls: list[str] = []
        previous_fk_control = self.control_parent_group
        for index, joint in enumerate(segments):
            current_fk_ctrl: str = self.curve_instance.curve_circle(name=f"{joint}_CTRL", scale=scale)
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder[rotation_order].value)
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder[rotation_order].value)
            cmds.setAttr(f"{current_fk_ctrl}.overrideEnabled", True)
            cmds.setAttr(f"{current_fk_ctrl}.overrideRGBColors", True)
            cmds.setAttr(f"{current_fk_ctrl}.overrideColorRGB", 1, 1, 1)

            cmds.matchTransform(current_fk_ctrl, joint, position=True, rotation=True, scale=False)
            cmds.parent(current_fk_ctrl, previous_fk_control)

            bake_transform_to_offset_parent_matrix(current_fk_ctrl)

            if index == 0:
                cmds.connectAttr(f"{current_fk_ctrl}.worldMatrix[0]",
                                 f"{joint}.offsetParentMatrix")
            else:
                cmds.connectAttr(f"{current_fk_ctrl}.translate", f"{joint}.translate")
                cmds.connectAttr(f"{current_fk_ctrl}.rotate", f"{joint}.rotate")

            fk_ctrls.append(current_fk_ctrl)
            previous_fk_control = current_fk_ctrl

        return fk_ctrls
