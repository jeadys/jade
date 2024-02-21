import maya.cmds as cmds


class ArmRoll:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_arm_roll_locators(self):
        # Upper Arm
        loc_shoulder_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_shoulder_roll_aim")
        cmds.matchTransform(loc_shoulder_roll_aim, f"{self.prefix}_DEF_humerus", position=True, rotation=True,
                            scale=False)

        cmds.move(0, 0, -25, loc_shoulder_roll_aim, relative=True, objectSpace=True)

        # Lower Arm
        loc_wrist_roll_aim = cmds.spaceLocator(name=f"{self.prefix}_LOC_wrist_roll_aim")
        cmds.matchTransform(loc_wrist_roll_aim, f"{self.prefix}_DEF_wrist", position=True, rotation=True, scale=False)

        cmds.move(0, 0, -25, loc_wrist_roll_aim, relative=True, objectSpace=True)

    def create_arm_roll_joints(self):
        # Upper Arm
        mch_shoulder_roll_start = cmds.joint(radius=5, rotationOrder="zxy",
                                             name=f"{self.prefix}_MCH_shoulder_roll_start")
        cmds.matchTransform(mch_shoulder_roll_start, f"{self.prefix}_DEF_humerus", position=True, rotation=True,
                            scale=False)
        cmds.makeIdentity(mch_shoulder_roll_start, apply=True, rotate=True)

        mch_shoulder_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_shoulder_roll_end")
        shoulder_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_humerus", f"{self.prefix}_DEF_radius"], mch_shoulder_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.delete(shoulder_constraint)

        cmds.parent(mch_shoulder_roll_start, f"{self.prefix}_DEF_humerus")

        mch_shoulder_follow_start = cmds.duplicate(mch_shoulder_roll_start, parentOnly=True,
                                                   name=f"{self.prefix}_MCH_shoulder_follow_start")
        mch_shoulder_follow_end = cmds.duplicate(mch_shoulder_roll_end, parentOnly=True,
                                                 name=f"{self.prefix}_MCH_shoulder_follow_end")

        cmds.parent(mch_shoulder_follow_start, world=True)
        cmds.parent(mch_shoulder_follow_end, mch_shoulder_follow_start)
        cmds.parent(f"{self.prefix}_LOC_shoulder_roll_aim", mch_shoulder_follow_start)
        cmds.move(0, 0, -20, mch_shoulder_follow_start, relative=True, objectSpace=True)

        # Lower Arm
        mch_wrist_roll_start = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_wrist_roll_start")
        cmds.matchTransform(mch_wrist_roll_start, f"{self.prefix}_DEF_wrist", position=True, rotation=True, scale=False)
        cmds.makeIdentity(mch_wrist_roll_start, apply=True, rotate=True)

        mch_wrist_roll_end = cmds.joint(radius=5, rotationOrder="zxy", name=f"{self.prefix}_MCH_wrist_roll_end")
        wrist_constraint = cmds.parentConstraint(
            [f"{self.prefix}_DEF_wrist", f"{self.prefix}_DEF_radius"], mch_wrist_roll_end, maintainOffset=False,
            skipRotate=["x", "y", "z"]
        )
        cmds.pointConstraint(f"{self.prefix}_DEF_wrist", mch_wrist_roll_start, maintainOffset=False)
        cmds.delete(wrist_constraint)

        cmds.parent(mch_wrist_roll_start, f"{self.prefix}_DEF_radius")
        cmds.parent(mch_wrist_roll_end, f"{self.prefix}_DEF_radius")
        cmds.parent(f"{self.prefix}_LOC_wrist_roll_aim", f"{self.prefix}_DEF_wrist")

    def get_distance_between_joints(self, joint1, joint2):
        pass

    def create_arm_roll_constraints(self):
        # Upper Arm
        cmds.aimConstraint(
            f"{self.prefix}_DEF_radius",
            f"{self.prefix}_MCH_shoulder_roll_start",
            aimVector=[0, 1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_shoulder_roll_aim",
        )

        cmds.parentConstraint(f"{self.prefix}_DEF_clavicle", f"{self.prefix}_MCH_shoulder_follow_start",
                              maintainOffset=True)

        # Lower Arm
        cmds.aimConstraint(
            f"{self.prefix}_DEF_radius",
            f"{self.prefix}_MCH_wrist_roll_start",
            aimVector=[0, -1, 0],
            upVector=[0, 0, -1],
            worldUpType="object",
            worldUpObject=f"{self.prefix}_LOC_wrist_roll_aim",
        )

    def create_arm_roll_handles(self):
        # Upper Arm
        cmds.ikHandle(
            name=f"{self.prefix}_MCH_shoulder_follow_ikHandle",
            startJoint=f"{self.prefix}_MCH_shoulder_follow_start",
            endEffector=f"{self.prefix}_MCH_shoulder_follow_end",
            solver="ikRPsolver",
        )
        cmds.setAttr(f"{self.prefix}_MCH_shoulder_follow_ikHandle.poleVectorX", 0)
        cmds.setAttr(f"{self.prefix}_MCH_shoulder_follow_ikHandle.poleVectorY", 0)
        cmds.setAttr(f"{self.prefix}_MCH_shoulder_follow_ikHandle.poleVectorZ", 0)

        cmds.parent(f"{self.prefix}_MCH_shoulder_follow_ikHandle", f"{self.prefix}_DEF_radius")
        cmds.matchTransform(f"{self.prefix}_MCH_shoulder_follow_ikHandle", f"{self.prefix}_DEF_radius", position=True,
                            rotation=False, scale=False)

        # Lower Arm

    def create_arm_roll_hierarchy(self):
        pass

    def create_arm_roll_attributes(self):
        pass

    def create_arm_roll_nodes(self):
        _mch_arm_roll_multiply_node = cmds.createNode("multiplyDivide", name=f"{self.prefix}_MCH_arm_roll_multiply")

        # Upper Arm
        cmds.setAttr(f"{self.prefix}_MCH_arm_roll_multiply.input2.input2X", 0.5)
        cmds.connectAttr(f"{self.prefix}_DEF_humerus.rotate.rotateY",
                         f"{self.prefix}_MCH_arm_roll_multiply.input1.input1X")
        cmds.connectAttr(f"{self.prefix}_MCH_arm_roll_multiply.output.outputX",
                         f"{self.prefix}_MCH_shoulder_roll_end.rotate.rotateY")

        # Lower Arm
        cmds.setAttr(f"{self.prefix}_MCH_arm_roll_multiply.input2.input2Y", 0.5)
        cmds.connectAttr(f"{self.prefix}_MCH_wrist_roll_start.rotate.rotateY",
                         f"{self.prefix}_MCH_arm_roll_multiply.input1.input1Y")
        cmds.connectAttr(f"{self.prefix}_MCH_arm_roll_multiply.output.outputY",
                         f"{self.prefix}_MCH_wrist_roll_end.rotate.rotateY")


if __name__ == "__main__":
    pass
