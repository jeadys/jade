import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton
from modular.mechanisms.limb_stretch import Stretch

from utilities.bake_transform import bake_transform_to_offset_parent_matrix

from typing import Literal

from utilities.curve import select_curve
from utilities.enums import Shape


class Arm:
    name = "arm"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments)
        self.ik_chain: IKChain = IKChain(node=node, name=Arm.name)
        self.fk_chain: FKChain = FKChain(node=node, name=Arm.name)
        self.stretch: Stretch = Stretch(node=node, name=Arm.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(prefix=self.prefix)
        self.skeleton.orient_skeleton(prefix=self.prefix)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(prefix=self.prefix, segments=self.segments[1:])
        self.fk_controls = self.fk_chain.fk_control(prefix=self.prefix, segments=self.segments[1:])

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(prefix=self.prefix, segments=self.segments[1:])
        self.ik_controls = self.ik_chain.ik_control(prefix=self.prefix, segments=self.segments[1:])
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(prefix=self.prefix, fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints,
                                       ik_controls=self.ik_controls)

    def clavicle_control(self) -> None:
        clavicle_control = select_curve(shape=Shape.CUBE,
                                        name=f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_CTRL", scale=5)
        cmds.parent(clavicle_control, f"{self.prefix}{Arm.name}_{self.blueprint_nr}_CONTROL_GROUP")
        cmds.matchTransform(clavicle_control, f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_JNT", position=True,
                            rotation=True, scale=False)
        cmds.parentConstraint(clavicle_control, f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_JNT",
                              maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{Arm.name}_{self.blueprint_nr}_IK_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{Arm.name}_{self.blueprint_nr}_IK_GROUP",
                                  maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{Arm.name}_{self.blueprint_nr}_FK_CTRL_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{Arm.name}_{self.blueprint_nr}_FK_CTRL_GROUP",
                                  maintainOffset=True)

        if self.selection:
            clavicle_group = cmds.group(empty=True, name="clavicle_GROUP")
            cmds.matchTransform(clavicle_group, clavicle_control, position=True, rotation=True, scale=False)
            cmds.parent(clavicle_control, clavicle_group)

            if cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                cmds.parentConstraint(f"{self.prefix}{self.selection[0]}_JNT", clavicle_group, maintainOffset=True)
            elif cmds.objExists(f"{self.prefix}{self.selection[0]}_JNT"):
                cmds.parentConstraint(f"{self.selection[0]}_JNT", clavicle_group, maintainOffset=True)

            cmds.parent(clavicle_group, f"{self.prefix}{Arm.name}_{self.blueprint_nr}_CONTROL_GROUP")

        bake_transform_to_offset_parent_matrix(clavicle_control)

    def generate_arm(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()
        self.clavicle_control()

    def stretch_arm(self) -> None:
        self.stretch.stretch_joint(prefix=self.prefix, segments=self.segments[1:])
        self.stretch.stretch_attribute(prefix=self.prefix)
        self.stretch.stretch_node(prefix=self.prefix, segments=self.segments[1:])
