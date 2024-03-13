import maya.cmds as cmds


class LegRoll:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_leg_roll_constraints(self) -> None:
        # Upper Part Of Leg
        cmds.aimConstraint(
            f"{self.prefix}_DEF_lowerleg",
            f"{self.prefix}_MCH_upperleg_roll_start",
            aimVector=[0, 1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_upperleg_roll_aim",
        )

        cmds.parentConstraint(f"{self.prefix}_DEF_upperleg", f"{self.prefix}_MCH_upperleg_follow_start",
                              maintainOffset=True)

        # Lower Part Of Leg
        cmds.aimConstraint(
            f"{self.prefix}_DEF_lowerleg",
            f"{self.prefix}_MCH_ankle_roll_start",
            aimVector=[0, -1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_ankle_roll_aim",
        )

    def create_leg_roll_handles(self) -> None:
        # Upper Part Of Leg
        cmds.ikHandle(
            name=f"{self.prefix}_MCH_upperleg_follow_ikHandle",
            startJoint=f"{self.prefix}_MCH_upperleg_follow_start",
            endEffector=f"{self.prefix}_MCH_upperleg_follow_end",
            solver="ikRPsolver",
        )

        cmds.setAttr(f"{self.prefix}_MCH_upperleg_follow_ikHandle.poleVectorX", 0)
        cmds.setAttr(f"{self.prefix}_MCH_upperleg_follow_ikHandle.poleVectorY", 0)
        cmds.setAttr(f"{self.prefix}_MCH_upperleg_follow_ikHandle.poleVectorZ", 0)

        cmds.parent(f"{self.prefix}_MCH_upperleg_follow_ikHandle", f"{self.prefix}_DEF_lowerleg")
        cmds.matchTransform(f"{self.prefix}_MCH_upperleg_follow_ikHandle", f"{self.prefix}_DEF_lowerleg", position=True,
                            rotation=False, scale=False)

    def create_leg_roll_nodes(self) -> None:
        mch_leg_roll_multiply_node = cmds.createNode("multiplyDivide", name=f"{self.prefix}_MCH_leg_roll_multiply")

        # Upper Part Of Leg
        cmds.setAttr(f"{mch_leg_roll_multiply_node}.input2.input2X", 0.5)
        cmds.connectAttr(f"{self.prefix}_DEF_upperleg.rotate.rotateY",
                         f"{mch_leg_roll_multiply_node}.input1.input1X")
        cmds.connectAttr(f"{mch_leg_roll_multiply_node}.output.outputX",
                         f"{self.prefix}_MCH_upperleg_roll_end.rotate.rotateY")

        # Lower Part Of Leg
        cmds.setAttr(f"{mch_leg_roll_multiply_node}.input2.input2Y", 0.5)
        cmds.connectAttr(f"{self.prefix}_MCH_ankle_roll_start.rotate.rotateY",
                         f"{mch_leg_roll_multiply_node}.input1.input1Y")
        cmds.connectAttr(f"{mch_leg_roll_multiply_node}.output.outputY",
                         f"{self.prefix}_MCH_ankle_roll_end.rotate.rotateY")

    def create_leg_roll_locators(self) -> None:
        # Upper Part Of Leg
        loc_upperleg_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_upperleg_roll_aim")
        cmds.matchTransform(loc_upperleg_roll_aim, f"{self.prefix}_DEF_upperleg", position=True, rotation=True,
                            scale=False)
        cmds.move(0, 0, -25, loc_upperleg_roll_aim, relative=True, objectSpace=True)

        # Lower Part Of Leg
        loc_ankle_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_ankle_roll_aim")
        cmds.matchTransform(loc_ankle_roll_aim, f"{self.prefix}_DEF_ankle", position=True, rotation=True, scale=False)
        cmds.move(0, 0, -25, loc_ankle_roll_aim, relative=True, objectSpace=True)

    def create_leg_roll_joints(self) -> None:
        # Upper Part Of Leg
        mch_upperleg_roll_start = cmds.joint(radius=5, rotationOrder="zxy",
                                             name=f"{self.prefix}_MCH_upperleg_roll_start")
        cmds.matchTransform(mch_upperleg_roll_start, f"{self.prefix}_DEF_upperleg", position=True, rotation=True,
                            scale=False)
        cmds.makeIdentity(mch_upperleg_roll_start, apply=True, rotate=True)

        mch_upperleg_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_upperleg_roll_end")
        upper_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_upperleg", f"{self.prefix}_DEF_lowerleg"], mch_upperleg_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.delete(upper_constraint)

        cmds.parent(mch_upperleg_roll_start, f"{self.prefix}_DEF_upperleg")

        mch_upperleg_follow_start = cmds.duplicate(mch_upperleg_roll_start, parentOnly=True,
                                                   name=f"{self.prefix}_MCH_upperleg_follow_start")
        mch_upperleg_follow_end = cmds.duplicate(mch_upperleg_roll_end, parentOnly=True,
                                                 name=f"{self.prefix}_MCH_upperleg_follow_end")

        cmds.parent(mch_upperleg_follow_start, world=True)
        cmds.parent(mch_upperleg_follow_end, mch_upperleg_follow_start)
        cmds.parent(f"{self.prefix}_LOC_upperleg_roll_aim", mch_upperleg_follow_start)
        cmds.move(0, 0, -20, mch_upperleg_follow_start, relative=True, objectSpace=True)

        # Lower Part Of leg
        mch_ankle_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_ankle_roll_start")
        cmds.matchTransform(mch_ankle_roll_start, f"{self.prefix}_DEF_ankle", position=True, rotation=True,
                            scale=False)
        cmds.makeIdentity(mch_ankle_roll_start, apply=True, rotate=True)

        mch_ankle_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_ankle_roll_end")
        lower_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_ankle", f"{self.prefix}_DEF_lowerleg"], mch_ankle_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.pointConstraint(f"{self.prefix}_DEF_ankle", mch_ankle_roll_start, maintainOffset=False)
        cmds.delete(lower_constraint)

        cmds.parent(mch_ankle_roll_start, f"{self.prefix}_DEF_lowerleg")
        cmds.parent(mch_ankle_roll_end, f"{self.prefix}_DEF_lowerleg")
        cmds.parent(f"{self.prefix}_LOC_ankle_roll_aim", f"{self.prefix}_DEF_ankle")


if __name__ == "__main__":
    pass
