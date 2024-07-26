import maya.cmds as cmds

from data.rig_structure import Segment
from rig.kinematics.fk_chain import FKChain
from rig.kinematics.ik_chain import IKChain
from rig.kinematics.skeleton import Skeleton
from rig.mechanisms.limb_stretch import Stretch
from rig.mechanisms.limb_twist import Twist
from rig.mechanisms.ribbon import Ribbon
from utilities.enums import TwistFlow


class Leg:
    name = "leg"

    def __init__(self, node, segments: list[Segment]):
        self.node = node
        self.segments = segments

        self.skeleton: Skeleton = Skeleton(node=self.node)
        self.ik_chain: IKChain = IKChain(node=self.node, name=Leg.name)
        self.fk_chain: FKChain = FKChain(node=self.node, name=Leg.name)
        self.stretch: Stretch = Stretch(node=self.node, name=Leg.name)
        self.twist: Twist = Twist(node=self.node, name=Leg.name)
        self.ribbon: Ribbon = Ribbon(node=self.node, name=Leg.name)

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
        self.ik_controls = self.ik_chain.ik_control(segments=self.segments[:-2])
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def twist_mechanism(self) -> None:
        start, end = self.twist.twist_joint(parent_segment=self.segments[0], start_segment=self.segments[0],
                                            end_segment=self.segments[1], twist_flow=TwistFlow.FORWARD)
        self.twist.setup_twist_hierarchy(start_joint=start, end_joint=end)

        start, end = self.twist.twist_joint(parent_segment=self.segments[1], start_segment=self.segments[1],
                                            end_segment=self.segments[2], twist_flow=TwistFlow.BACKWARD)
        self.twist.setup_twist_hierarchy(start_joint=start, end_joint=end)

    def stretch_mechanism(self) -> None:
        self.stretch.stretch_joint(segments=self.segments[:-2])
        self.stretch.stretch_attribute()
        self.stretch.stretch_node(segments=self.segments[:-2])

    def ribbon_mechanism(self) -> None:
        self.ribbon.ribbon_plane(divisions=8, width=50, length=0.1)
        self.ribbon.ribbon_intermediate_controls(control_amount=1)
        self.ribbon.ribbon_tweak_controls(control_amount=2)
        self.ribbon.attach_ribbon_to_module(segments=self.segments[:-2])
        self.ribbon.add_sine_deform(main_control=self.ik_controls[0])
        self.ribbon.add_twist_deform(main_control=self.ik_controls[0])

    def generate_module(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()
        self.ribbon_mechanism()

        # if cmds.getAttr(f"{self.node}.twist"):
        #     self.twist_mechanism()
        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
