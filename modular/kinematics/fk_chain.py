import maya.cmds as cmds

from modular.biped.biped import Segment

from utilities.set_rgb_color import set_rgb_color
from utilities.curve import select_curve
from utilities.bake_transform import bake_transform_to_offset_parent_matrix


class FKChain:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def fk_joint(self, prefix, segments: list[Segment]) -> list[str]:
        joint_group = cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_FK_GROUP")

        joint_layer_group = f"{prefix}{self.name}_{self.blueprint_nr}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)
        cmds.parent(joint_group, joint_layer_group)

        fk_joints: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{prefix}{segment.name}_{self.blueprint_nr}_FK"):
                continue

            current_segment = cmds.duplicate(f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                             name=f"{prefix}{segment.name}_{self.blueprint_nr}_FK", parentOnly=True)[0]
            cmds.parentConstraint(current_segment, f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                  maintainOffset=True)

            if segment.control.parent is not None:
                cmds.parent(current_segment, f"{prefix}{segment.parent.name}_{self.blueprint_nr}_FK")
            else:
                cmds.parent(current_segment, joint_group)

            fk_joints.append(current_segment)

        return fk_joints

    def fk_control(self, prefix, segments: list[Segment]) -> list[str]:
        control_group = cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_FK_CTRL_GROUP")

        joint_control_group = f"{prefix}{self.name}_{self.blueprint_nr}_CONTROL_GROUP"
        if not cmds.objExists(joint_control_group):
            cmds.group(empty=True, name=joint_control_group)
        cmds.parent(control_group, joint_control_group)

        fk_controls: list[str] = []
        for segment in segments:
            if cmds.objExists(f"{prefix}{segment.name}_{self.blueprint_nr}_FK_CTRL"):
                continue

            current_segment = f"{prefix}{segment.name}_{self.blueprint_nr}_FK" if cmds.objExists(
                f"{prefix}{segment.name}_{self.blueprint_nr}_FK") else f"{prefix}{segment.name}_{self.blueprint_nr}_JNT"

            control_shape = cmds.getAttr(f"{segment.name}_{self.blueprint_nr}.control_shape")
            control_color = cmds.getAttr(f"{segment.name}_{self.blueprint_nr}.control_color")
            control_scale = cmds.getAttr(f"{segment.name}_{self.blueprint_nr}.control_scale")

            current_control = select_curve(shape=control_shape,
                                           name=f"{prefix}{segment.name}_{self.blueprint_nr}_FK_CTRL",
                                           scale=control_scale)
            set_rgb_color(current_control, (1, 0, 1))

            cmds.matchTransform(current_control, current_segment, position=True, rotation=True, scale=False)
            cmds.parentConstraint(current_control, current_segment, maintainOffset=True)

            if segment.control.parent is not None:
                cmds.parent(current_control, f"{prefix}{segment.control.parent.name}_{self.blueprint_nr}_FK_CTRL")
            else:
                cmds.parent(current_control, control_group)

            bake_transform_to_offset_parent_matrix(current_control)

            fk_controls.append(current_control)

        if self.selection and cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{prefix}{self.selection[0]}_JNT", control_group, maintainOffset=True)
        elif self.selection and not cmds.objExists(f"{prefix}{self.selection[0]}_JNT"):
            cmds.parentConstraint(f"{self.selection[0]}_JNT", control_group, maintainOffset=True)

        return fk_controls
