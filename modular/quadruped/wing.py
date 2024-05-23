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

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments)
        self.fk_chain: FKChain = FKChain(node=node, name=Wing.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []

    def base_skeleton(self):
        self.skeleton.generate_skeleton(prefix=self.prefix)
        self.skeleton.orient_skeleton(prefix=self.prefix)

    def forward_kinematic(self):
        self.fk_controls = self.fk_chain.fk_control(prefix=self.prefix, segments=self.segments)

    def generate_wing(self):
        self.base_skeleton()
        self.forward_kinematic()
