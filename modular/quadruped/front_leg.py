import maya.cmds as cmds

from modular.biped.biped import Segment
from modular.kinematics.ik_chain import IKChain
from modular.kinematics.fk_chain import FKChain
from modular.kinematics.skeleton import Skeleton
from modular.mechanisms.limb_stretch import Stretch
from modular.mechanisms.limb_twist import Twist

from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import TwistFlow

from typing import Literal


class FrontLeg:
    name = "front_leg"

    def __init__(self, node, segments: list[Segment], prefix: Literal["L_", "R_"] = ""):
        self.node = node
        self.segments = segments
        self.prefix = prefix
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

        self.skeleton: Skeleton = Skeleton(node=node, segments=segments)
        self.ik_chain: IKChain = IKChain(node=node, name=FrontLeg.name)
        self.fk_chain: FKChain = FKChain(node=node, name=FrontLeg.name)
        self.stretch: Stretch = Stretch(node=node, name=FrontLeg.name)
        self.twist: Twist = Twist(node=node, name=FrontLeg.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []

    def base_skeleton(self):
        self.skeleton.generate_skeleton(prefix=self.prefix)
        self.skeleton.orient_skeleton(prefix=self.prefix)

    def forward_kinematic(self):
        self.fk_joints = self.fk_chain.fk_joint(prefix=self.prefix, segments=self.segments[1:])
        self.fk_controls = self.fk_chain.fk_control(prefix=self.prefix, segments=self.segments[1:])

    def inverse_kinematic(self):
        self.ik_joints = self.ik_chain.ik_joint(prefix=self.prefix, segments=self.segments[1:])
        self.ik_controls = self.ik_chain.ik_control(prefix=self.prefix, segments=self.segments[1:])
        self.ik_chain.inverse_kinematic_space_swap(ik_control=self.ik_controls[0], pole_control=self.ik_controls[1])

    def switch_kinematic(self):
        self.ik_chain.switch_kinematic(prefix=self.prefix, fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def twist_mechanism(self) -> None:
        self.twist.twist_joint(prefix=self.prefix, parent_segment=self.segments[1], start_segment=self.segments[1],
                               end_segment=self.segments[2], twist_flow=TwistFlow.FORWARD)
        self.twist.twist_joint(prefix=self.prefix, parent_segment=self.segments[2], start_segment=self.segments[2],
                               end_segment=self.segments[3], twist_flow=TwistFlow.BACKWARD)

    def stretch_mechanism(self):
        self.stretch.stretch_joint(prefix=self.prefix, segments=self.segments[1:])
        self.stretch.stretch_attribute(prefix=self.prefix)
        self.stretch.stretch_node(prefix=self.prefix, segments=self.segments[1:])

    def clavicle_control(self):
        clavicle_control = cmds.circle(normal=(0, 1, 0), center=(0, 0, 0), radius=5, degree=1, sections=32,
                                       name=f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_CTRL")[0]
        cmds.parent(clavicle_control, f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_CONTROL_GROUP")
        cmds.matchTransform(clavicle_control, f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_JNT",
                            position=True,
                            rotation=True, scale=False)
        cmds.parentConstraint(clavicle_control, f"{self.prefix}{self.segments[0].name}_{self.blueprint_nr}_JNT",
                              maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_IK_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_IK_GROUP",
                                  maintainOffset=True)

        if cmds.objExists(f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_FK_CTRL_GROUP"):
            cmds.parentConstraint(clavicle_control, f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_FK_CTRL_GROUP",
                                  maintainOffset=True)

        if self.selection:
            clavicle_group = cmds.group(empty=True, name="clavicle_GROUP")
            cmds.matchTransform(clavicle_group, clavicle_control, position=True, rotation=True, scale=False)
            cmds.parent(clavicle_control, clavicle_group)
            cmds.parentConstraint(f"{self.prefix}{self.selection[0]}_JNT", clavicle_group, maintainOffset=True)
            cmds.parent(clavicle_group, f"{self.prefix}{FrontLeg.name}_{self.blueprint_nr}_CONTROL_GROUP")

        bake_transform_to_offset_parent_matrix(clavicle_control)

    def generate_front_leg(self):
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()
        self.clavicle_control()

        if cmds.getAttr(f"{self.node}.twist"):
            self.twist_mechanism()
        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
