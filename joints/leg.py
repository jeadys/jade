import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class LegSegment:
    name: str
    position: tuple[float, float, float]


class Leg:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, rotation_order, joint_orientation):
        self.prefix = prefix
        self.rotation_order = rotation_order
        self.orient_joint, self.orient_secondary_axis = joint_orientation.split(" - ", 1)
        side = 1 if self.prefix == "L" else -1
        self.leg_segments = (
            LegSegment(name=f"{self.prefix}_upperleg", position=(side * 10, 90, 0)),
            LegSegment(name=f"{self.prefix}_lowerleg", position=(side * 10, 50, 0)),
            LegSegment(name=f"{self.prefix}_ankle", position=(side * 10, 10, -7.5)),
            LegSegment(name=f"{self.prefix}_ball", position=(side * 10, 0, 0)),
            LegSegment(name=f"{self.prefix}_toe", position=(side * 10, 0, 7.5)),
        )

    def create_leg_locators(self) -> None:
        leg_locators_exist: bool = any(cmds.objExists(f"{locator.name}_LOC") for locator in self.leg_segments)

        if leg_locators_exist:
            cmds.error(f"L leg locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.leg_segments):
            current_locator = cmds.spaceLocator(name=f"{locator.name}_LOC")[0]
            cmds.setAttr(f"{current_locator}.overrideEnabled", True)
            cmds.setAttr(f"{current_locator}.overrideRGBColors", True)
            cmds.setAttr(f"{current_locator}.overrideColorRGB", 1, 1, 0)

            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_leg_joints(self) -> None:
        leg_joints_exist: bool = any(cmds.objExists(f"{joint.name}") for joint in self.leg_segments)
        leg_locators_exist: bool = any(cmds.objExists(f"{joint.name}_LOC") for joint in self.leg_segments)

        if leg_joints_exist:
            cmds.error(f"L leg joints already exist in {self.joint_parent_group}")

        if not leg_locators_exist:
            cmds.error(f"L leg locators are missing in {self.locator_parent_group}.")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.leg_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=3, rotationOrder=self.rotation_order, name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=False, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.leg_segments):
            if joint.name == self.leg_segments[-1].name or joint.name == self.leg_segments[-3].name:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint.name}", edit=True, orientJoint=self.orient_joint,
                           secondaryAxisOrient=self.orient_secondary_axis,
                           zeroScaleOrient=True)

        # if is_auto_parent and cmds.objExists("C_pelvis"):
        #     cmds.parent(f"{self.prefix}_upperleg", "C_pelvis")


if __name__ == "__main__":
    pass
