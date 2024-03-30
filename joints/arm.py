import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class ArmSegment:
    name: str
    position: tuple[float, float, float]


class Arm:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, rotation_order, joint_orientation):
        self.prefix = prefix
        self.rotation_order = rotation_order
        self.orient_joint, self.orient_secondary_axis = joint_orientation.split(" - ", 1)
        side = 1 if self.prefix == "L" else -1
        self.arm_segments = (
            ArmSegment(name=f"{self.prefix}_clavicle", position=(side * 5, 140, 7.5)),
            ArmSegment(name=f"{self.prefix}_upperarm", position=(side * 15, 140, -7.5)),
            ArmSegment(name=f"{self.prefix}_lowerarm", position=(side * 40, 140, -15)),
            ArmSegment(name=f"{self.prefix}_wrist", position=(side * 60, 140, -15)),
        )

    def create_arm_locators(self) -> None:
        arm_locators_exist: bool = any(cmds.objExists(f"{locator.name}_LOC") for locator in self.arm_segments)

        if arm_locators_exist:
            cmds.error(f"L arm locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.arm_segments):
            current_locator = cmds.spaceLocator(name=f"{locator.name}_LOC")[0]
            cmds.setAttr(f"{current_locator}.overrideEnabled", True)
            cmds.setAttr(f"{current_locator}.overrideRGBColors", True)
            cmds.setAttr(f"{current_locator}.overrideColorRGB", 1, 1, 0)

            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_arm_joints(self) -> None:
        arm_joints_exist: bool = any(cmds.objExists(f"{joint.name}") for joint in self.arm_segments)

        if arm_joints_exist:
            cmds.error(f"L arm joints already exist in {self.joint_parent_group}")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.arm_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=3, rotationOrder=self.rotation_order, name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=False, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.arm_segments):
            if joint.name == self.arm_segments[-1].name:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint.name}", edit=True, orientJoint=self.orient_joint,
                           secondaryAxisOrient=self.orient_secondary_axis,
                           zeroScaleOrient=True)


if __name__ == "__main__":
    pass
