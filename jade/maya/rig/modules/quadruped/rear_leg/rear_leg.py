import maya.cmds as cmds

from jade.maya.rig.meta_structure import Segment
from jade.maya.rig.kinematics.fk_chain import FKChain
from jade.maya.rig.kinematics.ik_chain import IKChain
from jade.maya.rig.kinematics.skeleton import Skeleton
from jade.maya.rig.mechanisms.limb_stretch import Stretch
from jade.maya.rig.mechanisms.limb_twist import Twist
from jade.maya.rig.mechanisms.ribbon import Ribbon


class RearLeg:
    name = "rear_leg"

    def __init__(self, node, segments: list[Segment]):
        self.node = node
        self.segments = segments

        self.skeleton: Skeleton = Skeleton(node=self.node)
        self.ik_chain: IKChain = IKChain(node=self.node, name=RearLeg.name)
        self.fk_chain: FKChain = FKChain(node=self.node, name=RearLeg.name)
        self.stretch: Stretch = Stretch(node=self.node, name=RearLeg.name)
        self.twist: Twist = Twist(node=self.node, name=RearLeg.name)
        self.ribbon: Ribbon = Ribbon(node=self.node, name=RearLeg.name)

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
        twist_amount = cmds.getAttr(f"{self.node}.twist_joints")
        self.twist.twist_joint(segments=self.segments[:-1], twist_amount=twist_amount)

    def stretch_mechanism(self) -> None:
        self.stretch.stretch_joint(segments=self.segments[:-1])
        self.stretch.stretch_attribute(main_control=self.ik_controls[0])
        self.stretch.stretch_node(segments=self.segments[:-1], main_control=self.ik_controls[0])

    def ribbon_mechanism(self) -> None:
        ribbon_divisions = cmds.getAttr(f"{self.node}.ribbon_divisions")
        ribbon_width = cmds.getAttr(f"{self.node}.ribbon_width")
        ribbon_length = cmds.getAttr(f"{self.node}.ribbon_length")
        ribbon_controls = cmds.getAttr(f"{self.node}.ribbon_controls")
        tweak_controls = cmds.getAttr(f"{self.node}.tweak_controls")
        self.ribbon.ribbon_plane(divisions=ribbon_divisions, width=ribbon_width, length=ribbon_length)
        self.ribbon.ribbon_intermediate_controls(control_amount=ribbon_controls)
        self.ribbon.ribbon_tweak_controls(control_amount=tweak_controls)
        self.ribbon.attach_ribbon_to_module(segments=self.segments[:-2])
        self.ribbon.add_sine_deform(main_control=self.ik_controls[0])
        self.ribbon.add_twist_deform(main_control=self.ik_controls[0])

    def generate_module(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()

        if cmds.attributeQuery("twist", node=self.node, exists=True) and cmds.getAttr(
                f"{self.node}.twist_enabled"):
            self.twist_mechanism()

        if cmds.attributeQuery("stretch", node=self.node, exists=True) and cmds.getAttr(
                f"{self.node}.stretch_enabled"):
            self.stretch_mechanism()

        if cmds.attributeQuery("ribbon", node=self.node, exists=True) and cmds.getAttr(
                f"{self.node}.ribbon_enabled"):
            self.ribbon_mechanism()
