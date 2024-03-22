import maya.cmds as cmds
import mechanisms.spine_stretch as spine_stretch_module
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import RotateOrder
from dataclasses import dataclass

reload(control_shape)
reload(spine_stretch_module)


@dataclass(frozen=True)
class SpineSegment:
    name: str
    shape: str


class FKSpine:
    def __init__(self, spine_segments) -> None:
        self.spine_segments = spine_segments
        self.kinematic_parent_group = "spine_kinematics"
        self.control_parent_group = "spine_controls"
        self.control_shape: Curve = Curve()

    def create_fk_spine(self):
        if len(self.spine_segments) < 3:
            return cmds.error("Spine should be at least 3 joints, e.g. pelvis, spine, neck")

        if self.spine_segments[0][0:2] not in ["C_", "M_"]:
            return cmds.error("Spine joints should be prefixed with either C_ or M_")

        self.create_fk_spine_joints()
        self.create_fk_spine_controls()

    def create_fk_spine_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_fk_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.spine_segments):
            current_fk_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_FK")[0]
            cmds.parentConstraint(current_fk_joint, joint, maintainOffset=True)
            cmds.parent(current_fk_joint, previous_fk_joint)

            bake_transform_to_offset_parent_matrix(current_fk_joint)

            previous_fk_joint = current_fk_joint

    def create_fk_spine_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        previous_fk_control = self.control_parent_group
        for index, joint in enumerate(self.spine_segments):
            current_fk_ctrl = self.control_shape.curve_circle(name=f"{joint}_FK_CTRL")
            cmds.setAttr(f"{current_fk_ctrl}.rotateOrder", RotateOrder.ZXY.value)
            cmds.matchTransform(current_fk_ctrl, joint, position=True, rotation=True, scale=False)
            cmds.parent(current_fk_ctrl, previous_fk_control)

            if index == 0:
                cmds.connectAttr(f"{joint}_FK_CTRL.worldMatrix[0]",
                                 f"{joint}_FK.offsetParentMatrix")
            else:
                cmds.connectAttr(f"{joint}_FK_CTRL.translate", f"{joint}_FK.translate")
                cmds.connectAttr(f"{joint}_FK_CTRL.rotate", f"{joint}_FK.rotate")

            bake_transform_to_offset_parent_matrix(current_fk_ctrl)

            previous_fk_control = current_fk_ctrl
