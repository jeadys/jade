import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class HandSegment:
    name: str
    count: int
    step: float
    position: tuple[float, float, float]


class Hand:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, rotation_order, joint_orientation):
        self.prefix = prefix
        self.rotation_order = rotation_order
        self.orient_joint, self.orient_secondary_axis = joint_orientation.split(" - ", 1)
        side = 1 if self.prefix == "L" else -1
        self.hand_segments = (
            HandSegment(name=f"{self.prefix}_thumb", count=3, step=side * 2.5, position=(side * 65, 137.5, -11)),
            HandSegment(name=f"{self.prefix}_index", count=4, step=side * 2.75, position=(side * 65, 140, -13)),
            HandSegment(name=f"{self.prefix}_middle", count=4, step=side * 3, position=(side * 65, 140, -15)),
            HandSegment(name=f"{self.prefix}_ring", count=4, step=side * 2.75, position=(side * 65, 140, -17)),
            HandSegment(name=f"{self.prefix}_pinky", count=4, step=side * 2.5, position=(side * 65, 140, -19))
        )

    def create_hand_locators(self):
        hand_locators_exist: bool = any(cmds.objExists(f"{locator.name}_LOC") for locator in self.hand_segments)

        if hand_locators_exist:
            cmds.error(f"L hand locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        for index, locator in enumerate(self.hand_segments):
            current_locator = cmds.spaceLocator(name=f"{locator.name}_LOC")[0]
            cmds.move(*locator.position, current_locator)
            if cmds.objExists(f"{self.prefix}_wrist_LOC"):
                cmds.parent(current_locator, f"{self.prefix}_wrist_LOC")
            else:
                cmds.parent(current_locator, world=True)

            previous_locator = current_locator
            for sub_index, sub_locator in enumerate(range(locator.count)):
                current_sub_locator = cmds.spaceLocator(name=f"{locator.name}_{sub_index}_LOC")[0]
                cmds.move(locator.position[0] + ((sub_index + 1) * locator.step), locator.position[1],
                          locator.position[2], current_sub_locator)
                cmds.parent(current_sub_locator, previous_locator)

                previous_locator = current_sub_locator

    def create_hand_joints(self) -> None:
        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        for index, joint in enumerate(self.hand_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=1, rotationOrder=self.rotation_order, name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=False, scale=False)
            if cmds.objExists(f"{self.prefix}_wrist"):
                cmds.parent(current_joint, f"{self.prefix}_wrist")
            else:
                cmds.parent(current_joint, world=True)

            previous_joint = current_joint
            for sub_index, sub_joint in enumerate(range(joint.count)):
                current_sub_joint = cmds.joint(radius=1, rotationOrder=self.rotation_order,
                                               name=f"{joint.name}_{sub_index}")
                cmds.matchTransform(current_sub_joint, f"{joint.name}_{sub_index}_LOC", position=True,
                                    rotation=False,
                                    scale=False)

                if sub_index == joint.count - 1:
                    cmds.joint(f"{current_sub_joint}", edit=True, orientJoint="none", zeroScaleOrient=True)
                else:
                    cmds.joint(f"{previous_joint}", edit=True, orientJoint=self.orient_joint,
                               secondaryAxisOrient=self.orient_secondary_axis,
                               zeroScaleOrient=True)

                previous_joint = current_sub_joint
