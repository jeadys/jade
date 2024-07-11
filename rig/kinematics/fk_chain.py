from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.check_relation import has_parent
from utilities.curve import select_curve
from utilities.enums import RotateOrder
from utilities.set_rgb_color import set_rgb_color


class FKChain:

    def __init__(self, node, name, prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.name = name
        self.prefix = prefix
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def fk_joint(self, segments: list[Segment]) -> list[str]:
        joint_group = f"{self.prefix}{self.name}_{self.module_nr}_FK_GROUP"
        if not cmds.objExists(joint_group):
            cmds.group(empty=True, name=joint_group)

        joint_layer_group = f"{self.prefix}{self.name}_{self.module_nr}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)

        if not has_parent(joint_group, joint_layer_group):
            cmds.parent(joint_group, joint_layer_group)

        fk_joints: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{self.prefix}{segment}_FK"):
                continue

            current_segment = cmds.duplicate(f"{self.prefix}{segment}_JNT",
                                             name=f"{self.prefix}{segment}_FK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{self.prefix}{segment}_JNT", maintainOffset=True)

            parent_joint = cmds.listConnections(f"{segment}.parent_joint")
            if parent_joint and cmds.objExists(f"{self.prefix}{parent_joint[0]}_FK"):
                cmds.parent(current_segment, f"{self.prefix}{parent_joint[0]}_FK")
            else:
                cmds.parent(current_segment, joint_group)

            fk_joints.append(current_segment)

        return fk_joints

    def fk_control(self, segments: list[Segment]) -> list[str]:
        control_group = f"{self.prefix}{self.name}_{self.module_nr}_FK_CTRL_GROUP"
        if not cmds.objExists(control_group):
            cmds.group(empty=True, name=control_group)

        joint_control_group = f"{self.prefix}{self.name}_{self.module_nr}_CONTROL_GROUP"
        if not cmds.objExists(joint_control_group):
            cmds.group(empty=True, name=joint_control_group)

        if not has_parent(control_group, joint_control_group):
            cmds.parent(control_group, joint_control_group)

        fk_controls: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{self.prefix}{segment}_FK_CTRL"):
                continue

            current_segment = f"{self.prefix}{segment}_FK" if cmds.objExists(
                f"{self.prefix}{segment}_FK") else f"{self.prefix}{segment}_JNT"

            control_shape = cmds.getAttr(f"{segment}.control_shape")
            control_color = cmds.getAttr(f"{segment}.control_color")
            control_scale = cmds.getAttr(f"{segment}.control_scale")

            current_control = select_curve(shape=control_shape,
                                           name=f"{self.prefix}{segment}_FK_CTRL",
                                           scale=control_scale)
            set_rgb_color(current_control, (1, 0, 1))
            cmds.setAttr(f"{current_control}.rotateOrder", RotateOrder.YZX)

            cmds.matchTransform(current_control, current_segment, position=True, rotation=True, scale=False)
            cmds.parentConstraint(current_control, current_segment, maintainOffset=True)

            parent_control = cmds.listConnections(f"{segment}.parent_joint")
            if parent_control and cmds.objExists(f"{self.prefix}{parent_control[0]}_FK_CTRL"):
                cmds.parent(current_control, f"{self.prefix}{parent_control[0]}_FK_CTRL")
            else:
                cmds.parent(current_control, control_group)

            bake_transform_to_offset_parent_matrix(current_control)

            fk_controls.append(current_control)

        if self.selection and cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.prefix}{self.selection[0]}_JNT", control_group, maintainOffset=True)
        elif self.selection and not cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)

        return fk_controls
