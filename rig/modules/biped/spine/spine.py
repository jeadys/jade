from typing import Literal

import maya.cmds as cmds

from data.rig_structure import Segment
from rig.kinematics.fk_chain import FKChain
from rig.kinematics.ik_chain import IKChain
from rig.kinematics.skeleton import Skeleton


class Spine:
    name = "spine"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=self.node, prefix=self.prefix)
        self.ik_chain: IKChain = IKChain(node=self.node, name=Spine.name, prefix=self.prefix)
        self.fk_chain: FKChain = FKChain(node=self.node, name=Spine.name, prefix=self.prefix)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(segments=self.segments)
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments)

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(segments=self.segments)
        self.ik_controls = self.ik_chain.spline_kinematic(segments=self.segments)

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def twist_mechanism(self) -> None:
        pass

    def stretch_mechanism(self) -> None:
        pass

    def generate_module(self) -> None:
        self.base_skeleton()
        # self.forward_kinematic()
        # self.inverse_kinematic()
        # self.switch_kinematic()
