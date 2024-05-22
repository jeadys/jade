import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton

from typing import Literal


class Spine:
    name = "spine"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments)
        self.ik_chain: IKChain = IKChain(node=node, name=Spine.name)
        self.fk_chain: FKChain = FKChain(node=node, name=Spine.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self):
        self.skeleton.generate_skeleton(prefix=self.prefix)
        self.skeleton.orient_skeleton(prefix=self.prefix)

    def forward_kinematic(self):
        self.fk_joints = self.fk_chain.fk_joint(prefix=self.prefix, segments=self.segments)
        self.fk_controls = self.fk_chain.fk_control(prefix=self.prefix, segments=self.segments)

    def inverse_kinematic(self):
        self.ik_joints = self.ik_chain.ik_joint(prefix=self.prefix, segments=self.segments)
        self.ik_controls = self.ik_chain.spline_kinematic(segments=self.segments)

    def switch_kinematic(self):
        self.ik_chain.switch_kinematic(prefix=self.prefix, fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def generate_spine(self):
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()
