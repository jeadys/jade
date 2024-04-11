import maya.cmds as cmds

from joints.joint import create_joints
from joints.locator import create_locators
from kinematics.fk_chain import FKChain
from kinematics.ik_chain import IKChain
from kinematics.fk_ik_switch import FKIKSwitch


class Leg:
    name: str = "leg"

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.side: int = 1 if self.prefix == "L" else -1
        self.segments: list[str] = [f"{self.prefix}_upperleg", f"{self.prefix}_lowerleg", f"{self.prefix}_ankle",
                                    f"{self.prefix}_ball", f"{self.prefix}_toe"]
        self.positions: list[tuple] = [(self.side * 10, 90, 0), (self.side * 10, 50, 0), (self.side * 10, 10, -7.5),
                                       (self.side * 10, 0, 0), (self.side * 10, 0, 7.5)]

    def create_leg_locators(self) -> list[str]:
        locators: list[str] = create_locators(self.segments, self.positions)

        return locators

    def create_leg_joints(self, rotation_order: str, joint_orientation: str) -> list[str]:
        joints: list[str] = create_joints(self.segments, rotation_order)

        # ORIENT CREATED JOINTS
        orient_joint, orient_secondary_axis = joint_orientation.split(" - ", 1)
        for index, joint in enumerate(self.segments):
            if joint == self.segments[-1]:
                cmds.joint(f"{joint}", edit=True, orientJoint="none", zeroScaleOrient=True)
            elif joint != self.segments[-3]:
                cmds.joint(f"{joint}", edit=True, orientJoint=orient_joint,
                           secondaryAxisOrient=orient_secondary_axis,
                           zeroScaleOrient=True)
        return joints

    def create_leg_controls(self, rotation_order: str):
        fk_instance = FKChain(prefix=self.prefix, name=Leg.name)
        fk_joints = fk_instance.create_fk_joints(segments=self.segments)
        fk_ctrls = fk_instance.create_fk_controls(segments=fk_joints[:-1], rotation_order=rotation_order, scale=5)

        ik_instance = IKChain(prefix=self.prefix, name=Leg.name)
        ik_joints = ik_instance.create_ik_joints(segments=self.segments)
        ik_ctrls = ik_instance.create_ik_controls(segments=ik_joints[:-2], rotation_order=rotation_order,
                                                  name=Leg.name, scale=5)

        switch_instance = FKIKSwitch(prefix=self.prefix, fk_joints=fk_joints, ik_joints=ik_joints, fk_ctrls=fk_ctrls,
                                     ik_ctrls=ik_ctrls, name=Leg.name)

        switch_instance.create_ik_fk_switch_control()


if __name__ == "__main__":
    pass
