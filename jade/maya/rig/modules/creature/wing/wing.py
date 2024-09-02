from jade.maya.rig.meta_structure import Segment
from jade.maya.rig.kinematics.fk_chain import FKChain
from jade.maya.rig.kinematics.skeleton import Skeleton


class Wing:
    name = "wing"

    def __init__(self, node, segments: list[Segment]):
        self.node = node
        self.segments = segments

        self.skeleton: Skeleton = Skeleton(node=self.node)
        self.fk_chain: FKChain = FKChain(node=self.node, name=Wing.name)

        self.fk_joints: list[str] = []
        self.fk_controls: list[str] = []

    def base_skeleton(self) -> None:
        self.skeleton.generate_skeleton(segments=self.segments)
        self.skeleton.orient_skeleton(segments=self.segments)

    def forward_kinematic(self) -> None:
        self.fk_controls = self.fk_chain.fk_control(segments=self.segments)

    def inverse_kinematic(self) -> None:
        pass

    def switch_kinematic(self) -> None:
        pass

    def twist_mechanism(self) -> None:
        pass

    def stretch_mechanism(self) -> None:
        pass

    def generate_module(self) -> None:
        self.base_skeleton()
        self.forward_kinematic()
