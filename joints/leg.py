import maya.cmds as cmds
from importlib import reload

import controllers.control_shape as control_shape
from mechanisms.leg_roll import LegRoll
from typing import Literal
from dataclasses import dataclass

reload(control_shape)


@dataclass(frozen=True)
class LegSegment:
    name: str
    position: tuple[float, float, float]


class Leg:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix: Literal["L", "R"]):
        self.prefix = prefix
        self.multiplier = 1 if self.prefix == "L" else -1
        self.leg_segments = (
            LegSegment(name="upperleg", position=(self.multiplier * 15, 145, 0)),
            LegSegment(name="lowerleg", position=(self.multiplier * 20, 80, 0)),
            LegSegment(name="ankle", position=(self.multiplier * 25, 15, -10)),
        )
        self.leg_roll: LegRoll = LegRoll(prefix=self.prefix)

    def create_leg_locators(self) -> None:
        leg_locators_exist: bool = any(cmds.objExists(f"{self.prefix}_LOC_{locator}") for locator in self.leg_segments)

        if leg_locators_exist:
            cmds.error(f"{self.prefix} leg locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.leg_segments):
            current_locator = cmds.spaceLocator(name=f"{self.prefix}_LOC_{locator.name}")
            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_leg_joints(self, is_auto_parent: bool, is_roll_limb: bool) -> None:
        leg_joints_exist: bool = any(cmds.objExists(f"{self.prefix}_DEF_{joint}") for joint in self.leg_segments)

        if leg_joints_exist:
            cmds.error(f"{self.prefix} leg joints already exist in {self.joint_parent_group}")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.leg_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_{joint.name}")
            cmds.matchTransform(current_joint, f"{self.prefix}_LOC_{joint.name}", position=True, rotation=True, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.leg_segments):
            if index == len(self.leg_segments) - 1:
                cmds.joint(f"{self.prefix}_DEF_{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{self.prefix}_DEF_{joint.name}", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                           zeroScaleOrient=True)

        if is_auto_parent and cmds.objExists("C_DEF_cog"):
            cmds.parent(f"{self.prefix}_DEF_upperleg", "C_DEF_cog")

        if is_roll_limb:
            self.leg_roll.create_leg_roll_locators()
            self.leg_roll.create_leg_roll_joints()
            self.leg_roll.create_leg_roll_handles()
            self.leg_roll.create_leg_roll_constraints()
            self.leg_roll.create_leg_roll_nodes()


if __name__ == "__main__":
    pass
