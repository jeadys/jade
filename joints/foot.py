import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class FootSegment:
    name: str
    position: tuple[float, float, float]


class Foot:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, rotation_order, joint_orientation):
        self.prefix = prefix
        self.rotation_order = rotation_order
        self.orient_joint, self.orient_secondary_axis = joint_orientation.split(" - ", 1)
        side = 1 if self.prefix == "L" else -1
        self.foot_segments = (
            FootSegment(name=f"{self.prefix}_bank_r_RF", position=(side * 5, 0, 0)),
            FootSegment(name=f"{self.prefix}_bank_l_RF", position=(side * 15, 0, 0)),
            FootSegment(name=f"{self.prefix}_heel_RF", position=(side * 10, 0, -10)),
            FootSegment(name=f"{self.prefix}_pivot_RF", position=(side * 10, 0, -2.5)),
            FootSegment(name=f"{self.prefix}_toe_RF", position=(side * 10, 0, 7.5)),
            FootSegment(name=f"{self.prefix}_ball_RF", position=(side * 10, 0, 0)),
            FootSegment(name=f"{self.prefix}_ankle_RF", position=(side * 10, 10, -7.5)),
        )

    def create_foot_locators(self) -> None:
        foot_locators_exist: bool = any(cmds.objExists(f"{locator.name}_LOC") for locator in self.foot_segments)

        if foot_locators_exist:
            cmds.error(f"L foot locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.foot_segments):
            current_locator = cmds.spaceLocator(name=f"{locator.name}_LOC")[0]

            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_foot_joints(self) -> None:
        foot_joints_exist: bool = any(cmds.objExists(f"{joint.name}") for joint in self.foot_segments)

        if foot_joints_exist:
            cmds.error(f"L foot joints already exist in {self.joint_parent_group}")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.foot_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=1, rotationOrder=self.rotation_order, name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=False, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.foot_segments[:-1]):
            if joint.name == f"{self.prefix}_bank_l_RF":
                cmds.joint(f"{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint.name}", edit=True, orientJoint=self.orient_joint,
                           secondaryAxisOrient=self.orient_secondary_axis,
                           zeroScaleOrient=True)
