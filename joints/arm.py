import maya.cmds as cmds
from importlib import reload

import mechanisms.arm_roll as arm_roll_module

reload(arm_roll_module)


class Arm:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_arm_locators(self):
        if cmds.objExists(f"{self.prefix}_LOC_arm_group"):
            return

        cmds.group(empty=True, name=f"{self.prefix}_LOC_arm_group")

        if not cmds.objExists("locators"):
            cmds.group(empty=True, name="locators")

        cmds.parent(f"{self.prefix}_LOC_arm_group", "locators")

        # Default start positions of the arm locators
        if self.prefix == "L":
            clavicle_move = (10, 225, 7.5)
            humerus_move = (25, 225, -10)
            radius_move = (55, 190, -17.5)
            wrist_move = (85, 155, 0)
        else:
            clavicle_move = (-10, 225, 7.5)
            humerus_move = (-25, 225, -10)
            radius_move = (-55, 190, -17.5)
            wrist_move = (-85, 155, 0)

        # clavicle
        loc_clavicle = cmds.spaceLocator(name=f"{self.prefix}_LOC_clavicle")
        cmds.scale(2, 2, 2, loc_clavicle)
        cmds.move(*clavicle_move, loc_clavicle)
        cmds.parent(loc_clavicle, f"{self.prefix}_LOC_arm_group")

        # humerus
        loc_humerus = cmds.spaceLocator(name=f"{self.prefix}_LOC_humerus")
        cmds.scale(2, 2, 2, loc_humerus)
        cmds.move(*humerus_move, loc_humerus)
        cmds.parent(loc_humerus, loc_clavicle)

        # radius
        loc_radius = cmds.spaceLocator(name=f"{self.prefix}_LOC_radius")
        cmds.scale(2, 2, 2, loc_radius)
        cmds.move(*radius_move, loc_radius)
        cmds.parent(loc_radius, loc_humerus)

        # wrist
        loc_wrist = cmds.spaceLocator(name=f"{self.prefix}_LOC_wrist")
        cmds.scale(2, 2, 2, loc_wrist)
        cmds.move(*wrist_move, loc_wrist)
        cmds.parent(loc_wrist, loc_radius)

    def create_arm_joints(self, is_auto_parent: bool, is_roll_limb: bool):
        if cmds.objExists(f"{self.prefix}_DEF_clavicle") and cmds.objExists(
                f"{self.prefix}_DEF_humerus") and cmds.objExists(f"{self.prefix}_DEF_radius") and cmds.objExists(
                f"{self.prefix}_DEF_wrist") or not cmds.objExists(f"{self.prefix}_LOC_arm_group"):
            return

        if not cmds.objExists("skeleton"):
            cmds.group(empty=True, name="skeleton")

        # Prevent Maya from auto parenting elements to newly created group
        cmds.select(deselect=True)

        # clavicle
        def_clavicle = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_clavicle")
        cmds.matchTransform(def_clavicle, f"{self.prefix}_LOC_clavicle", position=True, rotation=True, scale=False)

        # humerus
        def_humerus = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_humerus")
        cmds.matchTransform(def_humerus, f"{self.prefix}_LOC_humerus", position=True, rotation=True, scale=False)

        # radius
        def_radius = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_radius")
        cmds.matchTransform(def_radius, f"{self.prefix}_LOC_radius", position=True, rotation=True, scale=False)

        # wrist
        def_wrist = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_wrist")
        cmds.matchTransform(def_wrist, f"{self.prefix}_LOC_wrist", position=True, rotation=True, scale=False)

        # Parent joint chain
        cmds.parent(def_clavicle, "skeleton")

        # orient arm joints
        cmds.joint(f"{self.prefix}_DEF_clavicle", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_humerus", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_radius", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_wrist", edit=True, orientJoint="none", zeroScaleOrient=True)

        if is_auto_parent and cmds.objExists("DEF_spine_03"):
            cmds.parent(def_clavicle, "DEF_spine_03")

        if is_roll_limb:
            arm_roll_instance = arm_roll_module.ArmRoll(prefix=self.prefix)
            arm_roll_instance.create_arm_roll_locators()
            arm_roll_instance.create_arm_roll_joints()
            arm_roll_instance.create_arm_roll_handles()
            arm_roll_instance.create_arm_roll_constraints()
            arm_roll_instance.create_arm_roll_hierarchy()
            arm_roll_instance.create_arm_roll_nodes()


if __name__ == "__main__":
    pass
