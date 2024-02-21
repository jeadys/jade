import maya.cmds as cmds
from importlib import reload

import mechanisms.leg_roll as leg_roll_module

reload(leg_roll_module)


class Leg:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_leg_locators(self):
        if cmds.objExists(f"{self.prefix}_LOC_leg_group"):
            return

        cmds.group(empty=True, name=f"{self.prefix}_LOC_leg_group")

        if not cmds.objExists("locators"):
            cmds.group(empty=True, name="locators")

        cmds.parent(f"{self.prefix}_LOC_leg_group", "locators")

        # Default start positions of the leg locators
        if self.prefix == "L":
            position_femur = (15, 145, 0)
            position_tibia = (20, 80, 0)
            position_ankle = (25, 15, -10)
            position_ball = (25, 2.5, 0)
            position_ball_end = (25, 2.5, 20)
        else:
            position_femur = (-15, 145, 0)
            position_tibia = (-20, 80, 0)
            position_ankle = (-25, 15, -10)
            position_ball = (-25, 2.5, 0)
            position_ball_end = (-25, 2.5, 20)

        # femur
        loc_femur = cmds.spaceLocator(name=f"{self.prefix}_LOC_femur")
        cmds.scale(2, 2, 2, loc_femur)
        cmds.move(*position_femur, loc_femur)
        cmds.parent(loc_femur, f"{self.prefix}_LOC_leg_group")

        # tibia
        loc_tibia = cmds.spaceLocator(name=f"{self.prefix}_LOC_tibia")
        cmds.scale(2, 2, 2, loc_tibia)
        cmds.move(*position_tibia, loc_tibia)
        cmds.parent(loc_tibia, loc_femur)

        # ankle
        loc_ankle = cmds.spaceLocator(name=f"{self.prefix}_LOC_ankle")
        cmds.scale(2, 2, 2, loc_ankle)
        cmds.move(*position_ankle, loc_ankle)
        cmds.parent(loc_ankle, loc_tibia)

        # ball
        loc_ball = cmds.spaceLocator(name=f"{self.prefix}_LOC_ball")
        cmds.scale(2, 2, 2, loc_ball)
        cmds.move(*position_ball, loc_ball)
        cmds.parent(loc_ball, loc_ankle)

        # ball end
        loc_ball_end = cmds.spaceLocator(name=f"{self.prefix}_LOC_ball_end")
        cmds.scale(2, 2, 2, loc_ball_end)
        cmds.move(*position_ball_end, loc_ball_end)
        cmds.parent(loc_ball_end, loc_ball)

    def create_leg_joints(self, is_auto_parent: bool, is_roll_limb: bool):
        if cmds.objExists(f"{self.prefix}_DEF_femur") and cmds.objExists(f"{self.prefix}_DEF_tibia") and cmds.objExists(
                f"{self.prefix}_DEF_ankle") and cmds.objExists(f"{self.prefix}_DEF_ball") and cmds.objExists(
                f"{self.prefix}_DEF_ball_end") or not cmds.objExists(f"{self.prefix}_LOC_leg_group"):
            return

        if not cmds.objExists("skeleton"):
            cmds.group(empty=True, name="skeleton")

        # Prevent Maya from auto parenting elements to newly created group
        cmds.select(deselect=True)

        # femur
        def_femur = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_femur")
        cmds.matchTransform(def_femur, f"{self.prefix}_LOC_femur", position=True, rotation=True, scale=False)

        # tibia
        def_tibia = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_tibia")
        cmds.matchTransform(def_tibia, f"{self.prefix}_LOC_tibia", position=True, rotation=True, scale=False)

        # ankle
        def_ankle = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_ankle")
        cmds.matchTransform(def_ankle, f"{self.prefix}_LOC_ankle", position=True, rotation=True, scale=False)

        # ball
        def_ball = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_ball")
        cmds.matchTransform(def_ball, f"{self.prefix}_LOC_ball", position=True, rotation=True, scale=False)

        # ball end
        def_ball_end = cmds.joint(radius=3, rotationOrder="zxy", name=f"{self.prefix}_DEF_ball_end")
        cmds.matchTransform(def_ball_end, f"{self.prefix}_LOC_ball_end", position=True, rotation=True, scale=False)

        # Parent joint chain
        cmds.parent(def_femur, "skeleton")

        # orient leg joints
        cmds.joint(f"{self.prefix}_DEF_femur", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_tibia", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_ball", edit=True, orientJoint="yzx", secondaryAxisOrient="zup",
                   zeroScaleOrient=True)
        cmds.joint(f"{self.prefix}_DEF_ball_end", edit=True, orientJoint="none", zeroScaleOrient=True)

        if is_auto_parent and cmds.objExists("DEF_cog"):
            cmds.parent(def_femur, "DEF_cog")

        if is_roll_limb:
            leg_roll_instance = leg_roll_module.LegRoll(prefix=self.prefix)
            leg_roll_instance.create_leg_roll_locators()
            leg_roll_instance.create_leg_roll_joints()
            leg_roll_instance.create_leg_roll_handles()
            leg_roll_instance.create_leg_roll_constraints()
            leg_roll_instance.create_leg_roll_hierarchy()
            leg_roll_instance.create_leg_roll_nodes()


if __name__ == "__main__":
    pass
