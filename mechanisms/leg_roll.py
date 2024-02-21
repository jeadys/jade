import maya.cmds as cmds


class LegRoll:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_leg_roll_locators(self):
        # UPPER LEG
        loc_thigh_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_thigh_roll_aim")
        cmds.matchTransform(loc_thigh_roll_aim, f"{self.prefix}_DEF_femur", position=True, rotation=True, scale=False)

        cmds.move(0, 0, -25, loc_thigh_roll_aim, relative=True, objectSpace=True)

        # LOWER LEG
        loc_ankle_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_ankle_roll_aim")
        cmds.matchTransform(loc_ankle_roll_aim, f"{self.prefix}_DEF_ankle", position=True, rotation=True, scale=False)

        cmds.move(0, 0, -25, loc_ankle_roll_aim, relative=True, objectSpace=True)

    def create_leg_roll_joints(self):
        # UPPER LEG
        mch_thigh_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_thigh_roll_start")
        cmds.matchTransform(mch_thigh_roll_start, f"{self.prefix}_DEF_femur", position=True, rotation=True, scale=False)
        cmds.makeIdentity(mch_thigh_roll_start, apply=True, rotate=True)

        mch_thigh_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_thigh_roll_end")
        thigh_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_femur", f"{self.prefix}_DEF_tibia"], mch_thigh_roll_end, maintainOffset=False, skipRotate=["x", "y", "z"]
        )
        cmds.delete(thigh_constraint)

        cmds.parent(mch_thigh_roll_start, f"{self.prefix}_DEF_femur")

        mch_thigh_follow_start = cmds.duplicate(mch_thigh_roll_start, parentOnly=True, name=f"{self.prefix}_MCH_thigh_follow_start")
        mch_thigh_follow_end = cmds.duplicate(mch_thigh_roll_end, parentOnly=True, name=f"{self.prefix}_MCH_thigh_follow_end")
        cmds.parent(mch_thigh_follow_start, world=True)
        cmds.parent(mch_thigh_follow_end, mch_thigh_follow_start)
        cmds.parent(f"{self.prefix}_LOC_thigh_roll_aim", mch_thigh_follow_start)
        cmds.move(0, 0, -20, mch_thigh_follow_start, relative=True, objectSpace=True)

        # LOWER LEG
        mch_ankle_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_ankle_roll_start")
        cmds.matchTransform(mch_ankle_roll_start, f"{self.prefix}_DEF_ankle", position=True, rotation=True, scale=False)
        cmds.makeIdentity(mch_ankle_roll_start, apply=True, rotate=True)

        mch_ankle_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_ankle_roll_end")
        ankle_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_ankle", f"{self.prefix}_DEF_tibia"], mch_ankle_roll_end, maintainOffset=False, skipRotate=["x", "y", "z"]
        )
        cmds.pointConstraint(f"{self.prefix}_DEF_ankle", mch_ankle_roll_start, maintainOffset=False)
        cmds.delete(ankle_constraint)

        cmds.parent(mch_ankle_roll_start, f"{self.prefix}_DEF_tibia")
        cmds.parent(mch_ankle_roll_end, f"{self.prefix}_DEF_tibia")
        cmds.parent(f"{self.prefix}_LOC_ankle_roll_aim", f"{self.prefix}_DEF_ankle")

    def get_distance_between_joints(self, joint1, joint2):
        pass

    def create_leg_roll_constraints(self):
        # UPPER LEG
        cmds.aimConstraint(
            f"{self.prefix}_DEF_tibia",
            f"{self.prefix}_MCH_thigh_roll_start",
            aimVector=[0, 1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_thigh_roll_aim",
        )

        # cmds.parentConstraint("DEF_cog", "L_MCH_thigh_follow_start", maintainOffset=True)

        # LOWER LEG
        cmds.aimConstraint(
            f"{self.prefix}_DEF_tibia",
            f"{self.prefix}_MCH_ankle_roll_start",
            aimVector=[0, 1, 0],
            upVector=[-1, 0, 0],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_ankle_roll_aim",
        )

    def create_leg_roll_handles(self):
        # UPPER LEG
        cmds.ikHandle(
            name=f"{self.prefix}_MCH_thigh_follow_ikHandle",
            startJoint=f"{self.prefix}_MCH_thigh_follow_start",
            endEffector=f"{self.prefix}_MCH_thigh_follow_end",
            solver="ikRPsolver",
        )
        cmds.setAttr(f"{self.prefix}_MCH_thigh_follow_ikHandle.poleVectorX", 0)
        cmds.setAttr(f"{self.prefix}_MCH_thigh_follow_ikHandle.poleVectorY", 0)
        cmds.setAttr(f"{self.prefix}_MCH_thigh_follow_ikHandle.poleVectorZ", 0)

        cmds.parent(f"{self.prefix}_MCH_thigh_follow_ikHandle", f"{self.prefix}_DEF_tibia")
        cmds.matchTransform(f"{self.prefix}_MCH_thigh_follow_ikHandle", f"{self.prefix}_DEF_tibia", position=True, rotation=False, scale=False)

        # LOWER LEG

    def create_leg_roll_hierarchy(self):
        pass

    def create_leg_roll_attributes(self):
        pass

    def create_leg_roll_nodes(self):
        l_mch_leg_roll_multiply_node = cmds.createNode("multiplyDivide", name=f"{self.prefix}_MCH_leg_roll_multiply")

        # UPPER LEG
        cmds.setAttr(f"{self.prefix}_MCH_leg_roll_multiply.input2.input2X", 0.5)
        cmds.connectAttr(f"{self.prefix}_DEF_femur.rotate.rotateY", f"{self.prefix}_MCH_leg_roll_multiply.input1.input1X")
        cmds.connectAttr(f"{self.prefix}_MCH_leg_roll_multiply.output.outputX", f"{self.prefix}_MCH_thigh_roll_end.rotate.rotateY")

        # LOWER LEG
        cmds.setAttr(f"{self.prefix}_MCH_leg_roll_multiply.input2.input2Y", 0.5)
        cmds.connectAttr(f"{self.prefix}_MCH_ankle_roll_start.rotate.rotateY", f"{self.prefix}_MCH_leg_roll_multiply.input1.input1Y")
        cmds.connectAttr(f"{self.prefix}_MCH_leg_roll_multiply.output.outputY", f"{self.prefix}_MCH_ankle_roll_end.rotate.rotateY")


if __name__ == "__main__":
    pass
