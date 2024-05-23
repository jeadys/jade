import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton
from modular.mechanisms.limb_stretch import Stretch

from typing import Literal


class ArachneLeg:
    name = "arachne_leg"

    def __init__(self, node: str, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments)
        self.ik_chain: IKChain = IKChain(node=node, name=ArachneLeg.name)
        self.fk_chain: FKChain = FKChain(node=node, name=ArachneLeg.name)
        self.stretch: Stretch = Stretch(node=node, name=ArachneLeg.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(prefix=self.prefix)
        self.skeleton.orient_skeleton(prefix=self.prefix)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(prefix=self.prefix, segments=self.segments)
        self.fk_controls = self.fk_chain.fk_control(prefix=self.prefix, segments=self.segments[:-1])

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(prefix=self.prefix, segments=self.segments)
        self.ik_controls = self.ik_chain.ik_control(prefix=self.prefix, segments=self.segments)
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(prefix=self.prefix, fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def generate_arachne_leg(self):
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()

    def stretch_arachne_leg(self):
        self.stretch.stretch_joint(prefix=self.prefix, segments=self.segments)
        self.stretch.stretch_attribute(prefix=self.prefix)
        self.stretch.stretch_node(prefix=self.prefix, segments=self.segments)
