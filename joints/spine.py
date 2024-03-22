import maya.cmds as cmds


class Spine:
    def __init__(self):
        pass

    @staticmethod
    def create_spine_locators():
        if cmds.objExists(f"LOC_spine_group"):
            return
        else:
            cmds.group(empty=True, name=f"LOC_spine_group")

        if cmds.objExists("locators"):
            cmds.parent(f"LOC_spine_group", "locators")
        else:
            cmds.group(empty=True, name="locators")
            cmds.parent(f"LOC_spine_group", "locators")

        # root
        loc_root = cmds.spaceLocator(name="LOC_root")
        cmds.scale(2, 2, 2, loc_root)
        cmds.move(0, 0, 0, loc_root)
        cmds.parent(loc_root, "LOC_spine_group")

        # cog
        loc_cog = cmds.spaceLocator(name="LOC_cog")
        cmds.scale(2, 2, 2, loc_cog)
        cmds.move(0, 150, 0, loc_cog)
        cmds.parent(loc_cog, loc_root)

        # pelvis
        loc_pelvis = cmds.spaceLocator(name="LOC_pelvis")
        cmds.scale(2, 2, 2, loc_pelvis)
        cmds.move(0, 150, 0, loc_pelvis)
        cmds.parent(loc_pelvis, loc_cog)

        # spine one
        loc_spine_one = cmds.spaceLocator(name="LOC_spine_01")
        cmds.scale(2, 2, 2, loc_spine_one)
        cmds.move(0, 170, 5, loc_spine_one)
        cmds.parent(loc_spine_one, loc_pelvis)

        # spine two
        loc_spine_two = cmds.spaceLocator(name="LOC_spine_02")
        cmds.scale(2, 2, 2, loc_spine_two)
        cmds.move(0, 190, 7.5, loc_spine_two)
        cmds.parent(loc_spine_two, loc_spine_one)

        # spine three
        loc_spine_three = cmds.spaceLocator(name="LOC_spine_03")
        cmds.scale(2, 2, 2, loc_spine_three)
        cmds.move(0, 210, 5, loc_spine_three)
        cmds.parent(loc_spine_three, loc_spine_two)

        # neck
        loc_neck = cmds.spaceLocator(name="LOC_neck")
        cmds.scale(2, 2, 2, loc_neck)
        cmds.move(0, 230, 0, loc_neck)
        cmds.parent(loc_neck, loc_spine_three)

    @staticmethod
    def create_spine_joints(is_auto_parent: bool):
        if not cmds.objExists("LOC_spine_group"):
            return

        if not cmds.objExists("skeleton"):
            cmds.group(empty=True, name="skeleton")

        # Prevent Maya from auto parenting elements to newly created group
        cmds.select(deselect=True)

        # root
        def_root = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_root")
        cmds.matchTransform(def_root, "LOC_root", position=True, rotation=True, scale=False)

        # cog
        def_cog = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_cog")
        cmds.matchTransform(def_cog, "LOC_cog", position=True, rotation=True, scale=False)

        # pelvis
        def_pelvis = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_pelvis")
        cmds.matchTransform(def_pelvis, "LOC_pelvis", position=True, rotation=True, scale=False)

        # spine one
        def_spine_one = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_spine_01")
        cmds.matchTransform(def_spine_one, "LOC_spine_01", position=True, rotation=True, scale=False)

        # spine two
        def_spine_two = cmds.joint(radius=3,  rotationOrder="zxy", name="DEF_spine_02")
        cmds.matchTransform(def_spine_two, "LOC_spine_02", position=True, rotation=True, scale=False)

        # spine three
        def_spine_three = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_spine_03")
        cmds.matchTransform(def_spine_three, "LOC_spine_03", position=True, rotation=True, scale=False)

        # neck
        def_neck = cmds.joint(radius=3, rotationOrder="zxy", name="DEF_neck")
        cmds.matchTransform(def_neck, "LOC_neck", position=True, rotation=False, scale=False)

        # Parent joint chain
        cmds.parent(def_root, "skeleton")

        # Orient spine joints
        cmds.joint("DEF_root", edit=True, orientJoint="none", zeroScaleOrient=True)
        cmds.joint("DEF_cog", edit=True, orientJoint="yzx", secondaryAxisOrient="zup", zeroScaleOrient=True)
        cmds.joint("DEF_pelvis", edit=True, orientJoint="yzx", secondaryAxisOrient="zup", zeroScaleOrient=True)
        cmds.joint("DEF_spine_01", edit=True, orientJoint="yzx", secondaryAxisOrient="zup", zeroScaleOrient=True)
        cmds.joint("DEF_spine_02", edit=True, orientJoint="yzx", secondaryAxisOrient="zup", zeroScaleOrient=True)
        cmds.joint("DEF_spine_03", edit=True, orientJoint="yzx", secondaryAxisOrient="zup", zeroScaleOrient=True)
        cmds.joint("DEF_neck", edit=True, orientJoint="none", zeroScaleOrient=True)

        if is_auto_parent and cmds.objExists("L_DEF_clavicle"):
            cmds.parent("L_DEF_clavicle", def_spine_three)
        if is_auto_parent and cmds.objExists("R_DEF_clavicle"):
            cmds.parent("R_DEF_clavicle", def_spine_three)
        if is_auto_parent and cmds.objExists("L_DEF_femur"):
            cmds.parent("L_DEF_femur", def_cog)
        if is_auto_parent and cmds.objExists("R_DEF_femur"):
            cmds.parent("R_DEF_femur", def_cog)


if __name__ == "__main__":
    pass
