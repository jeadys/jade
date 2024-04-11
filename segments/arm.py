import maya.cmds as cmds

from joints.joint import create_joints
from joints.locator import create_locators
import joints.joint as jt
import joints.locator as lc
from kinematics.fk_chain import FKChain
from kinematics.ik_chain import IKChain
from kinematics.fk_ik_switch import FKIKSwitch
from importlib import reload
reload(jt)
reload(lc)


class Arm:
    name: str = "arm"

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.side: int = 1 if self.prefix == "L" else -1
        self.segments: list[str] = [f"{self.prefix}_clavicle", f"{self.prefix}_upperarm", f"{self.prefix}_lowerarm",
                                    f"{self.prefix}_wrist"]
        self.positions: list[tuple] = [(self.side * 5, 140, 7.5), (self.side * 15, 140, -7.5),
                                       (self.side * 40, 140, -15), (self.side * 60, 140, -15)]

    def create_arm_locators(self) -> list[str]:
        locators: list[str] = create_locators(self.segments, self.positions)

        return locators

    def create_arm_joints(self, rotation_order: str, joint_orientation: str) -> list[str]:
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

    def create_arm_controls(self, rotation_order: str):
        fk_instance: FKChain = FKChain(prefix=self.prefix, name=Arm.name)
        fk_joints: list[str] = fk_instance.create_fk_joints(segments=self.segments[1:])
        fk_ctrls: list[str] = fk_instance.create_fk_controls(segments=fk_joints, rotation_order=rotation_order, scale=5)

        ik_instance: IKChain = IKChain(prefix=self.prefix, name=Arm.name)
        ik_joints: list[str] = ik_instance.create_ik_joints(segments=self.segments[1:])
        ik_ctrls: list[str] = ik_instance.create_ik_controls(segments=ik_joints, rotation_order=rotation_order,
                                                             name=Arm.name, scale=5)

        switch_instance: FKIKSwitch = FKIKSwitch(prefix=self.prefix, fk_joints=fk_joints, ik_joints=ik_joints,
                                                 fk_ctrls=fk_ctrls, ik_ctrls=ik_ctrls, name=Arm.name)

        switch_instance.create_ik_fk_switch_control()


if __name__ == "__main__":
    pass
