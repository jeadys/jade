import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton
from modular.mechanisms.limb_stretch import Stretch
from modular.mechanisms.limb_twist import Twist

from utilities.enums import TwistFlow

from typing import Literal


class RearLeg:
    name = "rear_leg"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=self.node, prefix=self.prefix)
        self.ik_chain: IKChain = IKChain(node=self.node, name=RearLeg.name, prefix=self.prefix)
        self.fk_chain: FKChain = FKChain(node=self.node, name=RearLeg.name, prefix=self.prefix)
        self.stretch: Stretch = Stretch(node=self.node, name=RearLeg.name, prefix=self.prefix)
        self.twist: Twist = Twist(node=self.node, name=RearLeg.name, prefix=self.prefix)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(segments=self.segments)
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments[:-1])

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(segments=self.segments)
        self.ik_controls = self.ik_chain.spring_kinematic(segments=self.segments)
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
        self.stretch.stretch_joint(segments=self.segments[:-1])
        self.stretch.stretch_attribute()
        self.stretch.stretch_node(segments=self.segments[:-1])

    def generate_rear_leg(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()

        if cmds.getAttr(f"{self.node}.twist"):
            self.twist_mechanism()
        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
