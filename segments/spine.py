import maya.cmds as cmds

from joints.joint import create_joints
from joints.locator import create_locators
from kinematics.fk_chain import FKChain
from kinematics.fk_ik_switch import FKIKSwitch
from kinematics.spline_chain import SplineChain


class Spine:
    name: str = "spine"

    def __init__(self, prefix, spine_count: int):
        self.prefix = prefix
        self.spine_count = spine_count
        self.distance_between_spines: float = 40 / (self.spine_count - 1)

        self.segments: list[str] = [f"{self.prefix}_spine_0{spine + 1}" for spine in range(self.spine_count)]
        self.positions: list[tuple] = [(0, 100 + (self.distance_between_spines * spine), 0) for spine in
                                       range(self.spine_count)]

    def create_spine_locators(self) -> list[str]:
        locators: list[str] = create_locators(self.segments, self.positions)

        return locators

    def create_spine_joints(self, rotation_order: str, joint_orientation: str) -> list[str]:
        joints: list[str] = create_joints(self.segments, rotation_order)

        # ORIENT CREATED JOINTS
        orient_joint, orient_secondary_axis = joint_orientation.split(" - ", 1)
        for index, joint in enumerate(self.segments):
            if joint == self.segments[-1]:
                cmds.joint(f"{joint}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint}", edit=True, orientJoint=orient_joint,
                           secondaryAxisOrient=orient_secondary_axis,
                           zeroScaleOrient=True)

        return joints

    def create_spine_controls(self, rotation_order: str):
        fk_instance = FKChain(prefix=self.prefix, name=Spine.name)
        fk_joints = fk_instance.create_fk_joints(segments=self.segments)
        fk_ctrls = fk_instance.create_fk_controls(segments=fk_joints, rotation_order=rotation_order, scale=5)

        spine_ik_instance = SplineChain(prefix=self.prefix, name=Spine.name)
        ik_joints = spine_ik_instance.create_spline_joints(segments=self.segments)
        spine_ik_instance.create_spline_curve(segments=self.segments)
        ik_ctrls = spine_ik_instance.create_spline_controls()

        switch_instance = FKIKSwitch(prefix=self.prefix, fk_joints=fk_joints, ik_joints=ik_joints, fk_ctrls=fk_ctrls,
                                     ik_ctrls=ik_ctrls, name=Spine.name)

        switch_instance.create_ik_fk_switch_control()


if __name__ == "__main__":
    pass
