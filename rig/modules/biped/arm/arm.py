from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from rig.kinematics.fk_chain import FKChain
from rig.kinematics.ik_chain import IKChain
from rig.kinematics.skeleton import Skeleton
from rig.mechanisms.limb_stretch import Stretch
from rig.mechanisms.limb_twist import Twist
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import select_curve
from utilities.enums import Shape, TwistFlow


class Arm:
    name = "arm"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=self.node, prefix=self.prefix)
        self.ik_chain: IKChain = IKChain(node=self.node, name=Arm.name, prefix=self.prefix)
        self.fk_chain: FKChain = FKChain(node=self.node, name=Arm.name, prefix=self.prefix)
        self.stretch: Stretch = Stretch(node=self.node, name=Arm.name, prefix=self.prefix)
        self.twist: Twist = Twist(node=self.node, name=Arm.name, prefix=self.prefix)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(segments=self.segments[1:])
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments[1:])

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(segments=self.segments[1:])
        self.ik_controls = self.ik_chain.ik_control(segments=self.segments[1:])
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def twist_mechanism(self) -> None:
        start, end = self.twist.twist_joint(parent_segment=self.segments[1], start_segment=self.segments[1],
                                            end_segment=self.segments[2], twist_flow=TwistFlow.FORWARD)
        self.twist.setup_twist_hierarchy(start_joint=start, end_joint=end)

        start, end = self.twist.twist_joint(parent_segment=self.segments[2], start_segment=self.segments[2],
                                            end_segment=self.segments[3], twist_flow=TwistFlow.BACKWARD)
        self.twist.setup_twist_hierarchy(start_joint=start, end_joint=end)

    def stretch_mechanism(self) -> None:
        self.stretch.stretch_joint(segments=self.segments[1:])
        self.stretch.stretch_attribute()
        self.stretch.stretch_node(segments=self.segments[1:])

    def clavicle_control(self) -> None:
        clavicle_control = select_curve(shape=Shape.CUBE,
                                        name=f"{self.prefix}{self.segments[0]}_CTRL", scale=5)
        cmds.parent(clavicle_control, f"{self.prefix}{Arm.name}_{self.module_nr}_CONTROL_GROUP")
        cmds.matchTransform(clavicle_control, f"{self.prefix}{self.segments[0]}_JNT",
                            position=True, rotation=True, scale=False)
        cmds.parentConstraint(clavicle_control, f"{self.prefix}{self.segments[0]}_JNT",
                              maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{Arm.name}_{self.module_nr}_IK_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{Arm.name}_{self.module_nr}_IK_GROUP",
                                  maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{Arm.name}_{self.module_nr}_FK_CTRL_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{Arm.name}_{self.module_nr}_FK_CTRL_GROUP",
                                  maintainOffset=True)

        if self.selection:
            clavicle_group = cmds.group(empty=True, name="clavicle_GROUP")
            cmds.matchTransform(clavicle_group, clavicle_control, position=True, rotation=True, scale=False)
            cmds.parent(clavicle_control, clavicle_group)

            if cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                cmds.parentConstraint(f"{self.prefix}{self.selection[0]}_JNT", clavicle_group, maintainOffset=True)
            elif cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                cmds.parentConstraint(f"{self.selection[0]}_JNT", clavicle_group, maintainOffset=True)

            cmds.parent(clavicle_group, f"{self.prefix}{Arm.name}_{self.module_nr}_CONTROL_GROUP")

        bake_transform_to_offset_parent_matrix(clavicle_control)

    def generate_module(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()
        self.clavicle_control()

        if cmds.getAttr(f"{self.node}.twist"):
            self.twist_mechanism()
        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
