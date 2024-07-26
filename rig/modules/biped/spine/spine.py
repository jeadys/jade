import maya.cmds as cmds

from data.rig_structure import Segment
from rig.kinematics.fk_chain import FKChain
from rig.kinematics.ik_chain import IKChain
from rig.kinematics.skeleton import Skeleton
from rig.mechanisms.spline_stretch import SplineStretch


class Spine:
    name = "spine"

    def __init__(self, node, segments: list[Segment]):
        self.node = node
        self.segments = segments

        self.skeleton: Skeleton = Skeleton(node=self.node)
        self.ik_chain: IKChain = IKChain(node=self.node, name=Spine.name)
        self.fk_chain: FKChain = FKChain(node=self.node, name=Spine.name)
        self.stretch: SplineStretch = SplineStretch(node=self.node, name=Spine.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []
        self.ik_joints: list[str] = []
        self.ik_controls: list[str] = []
        self.curve = None

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_joints = self.fk_chain.fk_joint(segments=self.segments)
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments)

    def inverse_kinematic(self) -> None:
        self.ik_joints = self.ik_chain.ik_joint(segments=self.segments)
        ik_controls, curve = self.ik_chain.spline_kinematic(segments=self.segments)
        self.ik_controls = ik_controls
        self.curve = curve

    def switch_kinematic(self) -> None:
        self.ik_chain.switch_kinematic(fk_joints=self.fk_joints, fk_controls=self.fk_controls,
                                       ik_joints=self.ik_joints, ik_controls=self.ik_controls)

    def twist_mechanism(self) -> None:
        pass

    def stretch_mechanism(self) -> None:
        self.stretch.stretch_attribute(main_control=self.ik_controls[0])
        self.stretch.stretch_node(segments=self.segments[1:], curve=self.curve, main_control=self.ik_controls[0])

    def generate_module(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
        self.inverse_kinematic()
        self.switch_kinematic()

        if cmds.getAttr(f"{self.node}.stretch"):
            self.stretch_mechanism()
