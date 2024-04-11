import maya.cmds as cmds

from joints.joint import create_joints
from joints.locator import create_locators
from kinematics.fk_chain import FKChain


class Finger:
    fingers: list[str] = ["thumb", "index", "middle", "ring", "pinky"]

    def __init__(self, prefix: str, current: int):
        self.prefix = prefix
        self.current = current
        self.finger_name: str = self.fingers[current]
        self.side: int = 1 if self.prefix == "L" else -1
        self.joint_count: int = 4
        self.segments: list[str] = [f"{self.prefix}_{self.finger_name}_{count:02d}" for count in
                                    range(self.joint_count)]
        self.positions: list[tuple] = [(self.side * (65 + (2.5 * x)), 140, -11 - (self.current * 2)) for x in
                                       range(self.joint_count)]

    def create_finger_locators(self) -> list[str]:
        locators = create_locators(self.segments, self.positions)

        return locators

    def create_finger_joints(self, rotation_order: str, joint_orientation: str) -> list[str]:
        joints = create_joints(self.segments, rotation_order)

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

    def create_finger_controls(self, rotation_order: str):
        fk_instance = FKChain(prefix=self.prefix, name=self.finger_name)
        fk_joints = fk_instance.create_fk_joints(segments=self.segments)
        fk_ctrls = fk_instance.create_fk_controls(segments=fk_joints[:-1], rotation_order=rotation_order, scale=1)

        # ik_instance = IKChain(prefix=self.prefix, name=self.finger_name)
        # ik_joints = ik_instance.create_ik_joints(segments=self.segments)
        # ik_ctrls = ik_instance.create_ik_controls(segments=ik_joints, rotation_order=rotation_order, name=self.finger_name, scale=1)
        #
        # switch_instance = FKIKSwitch(prefix=self.prefix, fk_joints=fk_joints, ik_joints=ik_joints,
        #                                                fk_ctrls=fk_ctrls, ik_ctrls=ik_ctrls, name=self.finger_name)
        #
        # switch_instance.create_ik_fk_switch_control()

        cmds.parentConstraint(f"{self.prefix}_wrist", f"{self.prefix}_{self.finger_name}_controls", maintainOffset=True)


if __name__ == "__main__":
    pass
