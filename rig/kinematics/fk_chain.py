from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.check_relation import has_parent
from utilities.enums import RotateOrder
from utilities.set_rgb_color import set_rgb_color


class FKChain:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def fk_joint(self, segments: list[Segment]) -> list[str]:
        joint_group = f"{self.prefix}_FK_GROUP"
        if not cmds.objExists(joint_group):
            cmds.group(empty=True, name=joint_group)

        joint_layer_group = f"{self.prefix}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)

        if not has_parent(joint_group, joint_layer_group):
            cmds.parent(joint_group, joint_layer_group)

        fk_joints: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{segment}_FK"):
                continue

            current_segment = cmds.duplicate(f"{segment}_JNT", name=f"{segment}_FK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{segment}_JNT", maintainOffset=True)

            parent_joint = cmds.listRelatives(segment, parent=True, shapes=False, type="transform")
            if parent_joint and cmds.objExists(f"{parent_joint[0]}_FK"):
                cmds.parent(current_segment, f"{parent_joint[0]}_FK")
            else:
                cmds.parent(current_segment, joint_group)

            fk_joints.append(current_segment)

        return fk_joints

    def fk_control(self, segments: list[Segment]) -> list[str]:
        control_group = f"{self.prefix}_FK_CTRL_GROUP"
        if not cmds.objExists(control_group):
            cmds.group(empty=True, name=control_group)

        joint_control_group = f"{self.prefix}_CONTROL_GROUP"
        if not cmds.objExists(joint_control_group):
            cmds.group(empty=True, name=joint_control_group)

        if not has_parent(control_group, joint_control_group):
            cmds.parent(control_group, joint_control_group)

        fk_controls: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{segment}_FK_CTRL"):
                continue

            control_rgb = cmds.getAttr(f"{segment}.control_rgb")
            control_points = cmds.getAttr(f"{segment}.control_points")
            current_control = cmds.curve(name=f"{segment}_FK_CTRL", pointWeight=control_points, degree=1)

            set_rgb_color(node=current_control, color=control_rgb[0])
            cmds.setAttr(f"{current_control}.rotateOrder", RotateOrder.XYZ)

            cmds.matchTransform(current_control, f"{segment}_FK", position=True, rotation=True, scale=False)
            cmds.parentConstraint(current_control, f"{segment}_FK", maintainOffset=True)

            parent_control = cmds.listRelatives(segment, parent=True, shapes=False, type="transform")
            if parent_control and cmds.objExists(f"{parent_control[0]}_FK_CTRL"):
                cmds.parent(current_control, f"{parent_control[0]}_FK_CTRL")
            else:
                cmds.parent(current_control, control_group)

            bake_transform_to_offset_parent_matrix(current_control)

            fk_controls.append(current_control)

        if self.selection and cmds.objExists(f"{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)
        elif self.selection and not cmds.objExists(f"{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)

        return fk_controls
