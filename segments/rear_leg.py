import maya.cmds as cmds

from joints.joint import create_joints
from joints.locator import create_locators
from kinematics.fk_chain import FKChain
from kinematics.ik_chain import IKChain
from kinematics.fk_ik_switch import FKIKSwitch


class RearLeg:
    name: str = "rear_leg"

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.side: int = 1 if self.prefix == "L" else -1
        self.segments: list[str] = [f"{self.prefix}_quad_hip", f"{self.prefix}_quad_knee", f"{self.prefix}_quad_heel",
                                    f"{self.prefix}_quad_foot"]
        self.positions: list[tuple] = [(self.side * 5, 40, -25), (self.side * 5, 25, -22.5), (self.side * 5, 15, -35),
                                       (self.side * 5, 0, -35), (self.side * 5, 0, 20)]

    def create_leg_locators(self) -> list[str]:
        locators = create_locators(self.segments, self.positions)

        return locators

    def create_leg_joints(self, rotation_order: str, joint_orientation: str) -> list[str]:
        joints = create_joints(self.segments, rotation_order)

        # ORIENT CREATED JOINTS
        orient_joint, orient_secondary_axis = joint_orientation.split(" - ", 1)
        for index, joint in enumerate(self.segments):
            if joint != self.segments[-1]:
                cmds.joint(f"{joint}", edit=True, orientJoint=orient_joint,
                           secondaryAxisOrient=orient_secondary_axis,
                           zeroScaleOrient=True)

        return joints

    def create_leg_controls(self, rotation_order: str):
        fk_instance = FKChain(prefix=self.prefix, name=RearLeg.name)
        fk_joints = fk_instance.create_fk_joints(segments=self.segments)
        fk_ctrls = fk_instance.create_fk_controls(segments=fk_joints, rotation_order=rotation_order, scale=5)

        ik_instance = IKChain(prefix=self.prefix, name=RearLeg.name)
        ik_joints = ik_instance.create_ik_joints(segments=self.segments)
        ik_ctrls = ik_instance.create_ik_controls(segments=ik_joints, rotation_order=rotation_order, name=RearLeg.name,
                                                  scale=2.5)

        switch_instance = FKIKSwitch(prefix=self.prefix, fk_joints=fk_joints, ik_joints=ik_joints,
                                     fk_ctrls=fk_ctrls, ik_ctrls=ik_ctrls, name=RearLeg.name)

        switch_instance.create_ik_fk_switch_control()


if __name__ == "__main__":
    pass
