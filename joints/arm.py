import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class ArmSegment:
    name: str
    position: tuple[float, float, float]


class Arm:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix):
        self.prefix = prefix
        side = 1 if self.prefix == "L" else -1
        self.arm_segments = (
            ArmSegment(name=f"{self.prefix}_clavicle", position=(side * 10, 225, 7.5)),
            ArmSegment(name=f"{self.prefix}_upperarm", position=(side * 25, 225, -10)),
            ArmSegment(name=f"{self.prefix}_lowerarm", position=(side * 55, 225, -17.5)),
            ArmSegment(name=f"{self.prefix}_wrist", position=(side * 85, 225, -17.5)),
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
            current_joint = cmds.joint(radius=3, rotationOrder="zxy", name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=False, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.arm_segments):
            if index == len(self.arm_segments) - 1:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                           zeroScaleOrient=True)

        # if is_auto_parent and cmds.objExists("C_spine_03"):
        #     cmds.parent(f"{self.prefix}_clavicle", "C_spine_03")
