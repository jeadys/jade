import maya.cmds as cmds


class ArmRoll:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_arm_roll_constraints(self) -> None:
        # Upper Part Of Arm
        cmds.aimConstraint(
            f"{self.prefix}_DEF_lowerarm",
            f"{self.prefix}_MCH_upperarm_roll_start",
            aimVector=[0, 1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_upperarm_roll_aim",
        )

        cmds.parentConstraint(f"{self.prefix}_DEF_upperarm", f"{self.prefix}_MCH_upperarm_follow_start", maintainOffset=True)

        # Lower Part Of Arm
        cmds.aimConstraint(
            f"{self.prefix}_DEF_lowerarm",
            f"{self.prefix}_MCH_wrist_roll_start",
            aimVector=[0, -1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_wrist_roll_aim",
        )

    def create_arm_roll_handles(self) -> None:
        # Upper Part Of Arm
        cmds.ikHandle(
            name=f"{self.prefix}_MCH_upperarm_follow_ikHandle",
            startJoint=f"{self.prefix}_MCH_upperarm_follow_start",
            endEffector=f"{self.prefix}_MCH_upperarm_follow_end",
            solver="ikRPsolver",
        )

        cmds.setAttr(f"{self.prefix}_MCH_upperarm_follow_ikHandle.poleVectorX", 0)
        cmds.setAttr(f"{self.prefix}_MCH_upperarm_follow_ikHandle.poleVectorY", 0)
        cmds.setAttr(f"{self.prefix}_MCH_upperarm_follow_ikHandle.poleVectorZ", 0)

        cmds.parent(f"{self.prefix}_MCH_upperarm_follow_ikHandle", f"{self.prefix}_DEF_lowerarm")
        cmds.matchTransform(f"{self.prefix}_MCH_upperarm_follow_ikHandle", f"{self.prefix}_DEF_lowerarm", position=True,
                            rotation=False, scale=False)

    def create_arm_roll_nodes(self) -> None:
        mch_arm_roll_multiply_node = cmds.createNode("multiplyDivide", name=f"{self.prefix}_MCH_arm_roll_multiply")

        # Upper Part Of Arm
        cmds.setAttr(f"{mch_arm_roll_multiply_node}.input2.input2X", 0.5)
        cmds.connectAttr(f"{self.prefix}_DEF_upperarm.rotate.rotateY",
                         f"{mch_arm_roll_multiply_node}.input1.input1X")
        cmds.connectAttr(f"{mch_arm_roll_multiply_node}.output.outputX",
                         f"{self.prefix}_MCH_upperarm_roll_end.rotate.rotateY")

        # Lower Part Of arm
        cmds.setAttr(f"{mch_arm_roll_multiply_node}.input2.input2Y", 0.5)
        cmds.connectAttr(f"{self.prefix}_MCH_wrist_roll_start.rotate.rotateY",
                         f"{mch_arm_roll_multiply_node}.input1.input1Y")
        cmds.connectAttr(f"{mch_arm_roll_multiply_node}.output.outputY",
                         f"{self.prefix}_MCH_wrist_roll_end.rotate.rotateY")

    def create_arm_roll_locators(self) -> None:
        # Upper Part Of Arm
        loc_upperarm_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_upperarm_roll_aim")
        cmds.matchTransform(loc_upperarm_roll_aim, f"{self.prefix}_DEF_upperarm", position=True, rotation=True, scale=False)
        cmds.move(0, 0, -25, loc_upperarm_roll_aim, relative=True, objectSpace=True)

        # Lower Part Of Arm
        loc_wrist_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_wrist_roll_aim")
        cmds.matchTransform(loc_wrist_roll_aim, f"{self.prefix}_DEF_wrist", position=True, rotation=True, scale=False)
        cmds.move(0, 0, -25, loc_wrist_roll_aim, relative=True, objectSpace=True)

    def create_arm_roll_joints(self) -> None:
        # Upper Part Of Arm
        mch_upperarm_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_upperarm_roll_start")
        cmds.matchTransform(mch_upperarm_roll_start, f"{self.prefix}_DEF_upperarm", position=True, rotation=True,
                            scale=False)
        cmds.makeIdentity(mch_upperarm_roll_start, apply=True, rotate=True)

        mch_upperarm_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_upperarm_roll_end")
        upper_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_upperarm", f"{self.prefix}_DEF_lowerarm"], mch_upperarm_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.delete(upper_constraint)

        cmds.parent(mch_upperarm_roll_start, f"{self.prefix}_DEF_upperarm")

        mch_upperarm_follow_start = cmds.duplicate(mch_upperarm_roll_start, parentOnly=True,
                                          name=f"{self.prefix}_MCH_upperarm_follow_start")
        mch_upperarm_follow_end = cmds.duplicate(mch_upperarm_roll_end, parentOnly=True,
                                        name=f"{self.prefix}_MCH_upperarm_follow_end")

        cmds.parent(mch_upperarm_follow_start, world=True)
        cmds.parent(mch_upperarm_follow_end, mch_upperarm_follow_start)
        cmds.parent(f"{self.prefix}_LOC_upperarm_roll_aim", mch_upperarm_follow_start)
        cmds.move(0, 0, -20, mch_upperarm_follow_start, relative=True, objectSpace=True)

        # Lower Part Of Arm
        mch_wrist_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_wrist_roll_start")
        cmds.matchTransform(mch_wrist_roll_start, f"{self.prefix}_DEF_wrist", position=True, rotation=True,
                            scale=False)
        cmds.makeIdentity(mch_wrist_roll_start, apply=True, rotate=True)

        mch_wrist_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_wrist_roll_end")
        lower_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_wrist", f"{self.prefix}_DEF_lowerarm"], mch_wrist_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.pointConstraint(f"{self.prefix}_DEF_wrist", mch_wrist_roll_start, maintainOffset=False)
        cmds.delete(lower_constraint)

        cmds.parent(mch_wrist_roll_start, f"{self.prefix}_DEF_lowerarm")
        cmds.parent(mch_wrist_roll_end, f"{self.prefix}_DEF_lowerarm")
        cmds.parent(f"{self.prefix}_LOC_wrist_roll_aim", f"{self.prefix}_DEF_wrist")


if __name__ == "__main__":
    pass
