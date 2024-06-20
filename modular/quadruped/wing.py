import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton

from typing import Literal


class Wing:

    name = "wing"

    def __init__(self, node, segments: list[Segment],  prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments, prefix=self.prefix)
        self.fk_chain: FKChain = FKChain(node=node, name=Wing.name, prefix=self.prefix)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton()
        self.skeleton.orient_skeleton()

    def forward_kinematic(self) -> None:
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments)

    def generate_wing(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
