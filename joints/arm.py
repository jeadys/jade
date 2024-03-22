import maya.cmds as cmds
from importlib import reload

import controllers.control_shape as control_shape
from mechanisms.arm_roll import ArmRoll
import mechanisms.arm_roll as arm_roll
from typing import Literal
from dataclasses import dataclass

reload(arm_roll)
reload(control_shape)


@dataclass(frozen=True)
class ArmSegment:
    name: str
    shape: str
    position: tuple[float, float, float]


class Arm:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix: Literal["L", "R"]):
        self.prefix = prefix
        self.multiplier = 1 if self.prefix == "L" else -1
        self.arm_segments = (
            ArmSegment(name="clavicle", shape="circle", position=(self.multiplier * 10, 225, 7.5)),
            ArmSegment(name="upperarm", shape="circle", position=(self.multiplier * 25, 225, -10)),
            ArmSegment(name="lowerarm", shape="circle", position=(self.multiplier * 55, 190, -17.5)),
            ArmSegment(name="wrist", shape="star", position=(self.multiplier * 85, 155, 0)),
        )
        self.arm_roll: ArmRoll = ArmRoll(prefix=self.prefix)

    def create_arm_locators(self) -> None:
        arm_locators_exist: bool = any(cmds.objExists(f"{self.prefix}_LOC_{locator}") for locator in self.arm_segments)

        if arm_locators_exist:
            cmds.error(f"{self.prefix} arm locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.arm_segments):
            current_locator = cmds.spaceLocator(name=f"{self.prefix}_LOC_{locator.name}")
            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_arm_joints(self, is_auto_parent: bool, is_roll_limb: bool) -> None:
        arm_joints_exist: bool = any(cmds.objExists(f"{self.prefix}_DEF_{joint}") for joint in self.arm_segments)

        if arm_joints_exist:
            cmds.error(f"{self.prefix} arm joints already exist in {self.joint_parent_group}")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.arm_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_{joint.name}")
            cmds.matchTransform(current_joint, f"{self.prefix}_LOC_{joint.name}", position=True, rotation=True, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.arm_segments):
            if index == len(self.arm_segments) - 1:
                cmds.joint(f"{self.prefix}_DEF_{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{self.prefix}_DEF_{joint.name}", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                           zeroScaleOrient=True)

        if is_auto_parent and cmds.objExists("C_DEF_spine_03"):
            cmds.parent(f"{self.prefix}_DEF_clavicle", "C_DEF_spine_03")

        if is_roll_limb:
            self.arm_roll.create_arm_roll_locators()
            self.arm_roll.create_arm_roll_joints()
            self.arm_roll.create_arm_roll_handles()
            self.arm_roll.create_arm_roll_constraints()
            self.arm_roll.create_arm_roll_nodes()
