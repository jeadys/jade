import maya.cmds as cmds
from dataclasses import dataclass


@dataclass(frozen=True)
class SpineSegment:
    name: str
    position: tuple[float, float, float]


class Spine:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, spine_count):
        self.prefix = prefix
        self.spine_count = spine_count
        self.distance_between_spines = 40 / (self.spine_count - 1)  # Adjust for spacing between spines
        self.spine_segments = tuple(
            SpineSegment(name=f"{self.prefix}_spine_0{spine + 1}",
                         position=(0, 100 + (self.distance_between_spines * spine), 0))
            for spine in range(self.spine_count)
        )

    def create_spine_locators(self):
        spine_locators_exist: bool = any(cmds.objExists(f"{locator.name}_LOC") for locator in self.spine_segments)

        if spine_locators_exist:
            cmds.error(f"C spine locators already exist in {self.locator_parent_group}.")

        if not cmds.objExists(self.locator_parent_group):
            cmds.group(empty=True, name=self.locator_parent_group)

        previous_locator = self.locator_parent_group
        for index, locator in enumerate(self.spine_segments):
            current_locator = cmds.spaceLocator(name=f"{locator.name}_LOC")[0]
            cmds.setAttr(f"{current_locator}.overrideEnabled", True)
            cmds.setAttr(f"{current_locator}.overrideRGBColors", True)
            cmds.setAttr(f"{current_locator}.overrideColorRGB", 1, 1, 0)

            cmds.scale(2, 2, 2, current_locator)
            cmds.move(*locator.position, current_locator)
            cmds.parent(current_locator, previous_locator)

            previous_locator = current_locator

    def create_spine_joints(self):
        spine_joints_exist: bool = any(cmds.objExists(f"{joint.name}") for joint in self.spine_segments)

        if spine_joints_exist:
            cmds.error(f"C spine joints already exist in {self.joint_parent_group}")

        if not cmds.objExists(self.joint_parent_group):
            cmds.group(empty=True, name=self.joint_parent_group)

        previous_joint = self.joint_parent_group
        for index, joint in enumerate(self.spine_segments):
            # Prevent Maya from auto parenting joint to selected item in scene.
            cmds.select(deselect=True)
            current_joint = cmds.joint(radius=3, rotationOrder="zxy", name=f"{joint.name}")
            cmds.matchTransform(current_joint, f"{joint.name}_LOC", position=True, rotation=True, scale=False)
            cmds.parent(current_joint, previous_joint)

            previous_joint = current_joint

        for index, joint in enumerate(self.spine_segments):
            if index == len(self.spine_segments) - 1:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="none", zeroScaleOrient=True)
            else:
                cmds.joint(f"{joint.name}", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                           zeroScaleOrient=True)

        # if is_auto_parent and cmds.objExists("L_clavicle"):
        #     cmds.parent("L_clavicle", "C_spine_03")
        # if is_auto_parent and cmds.objExists("R_clavicle"):
        #     cmds.parent("R_clavicle", "C_spine_03")
        # if is_auto_parent and cmds.objExists("L_upperleg"):
        #     cmds.parent(f"L_upperleg", "C_pelvis")
        # if is_auto_parent and cmds.objExists("R_upperleg"):
        #     cmds.parent(f"R_upperleg", "C_pelvis")


if __name__ == "__main__":
    pass
