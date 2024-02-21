import maya.cmds as cmds

from utilities.enums import CONOperation, MUDOperation, PMAOperation


class FootRoll:
    def __init__(self, prefix):
        self.prefix = prefix

    def create_foot_roll_locators(self):
        # heel reverse
        loc_heel_reverse = cmds.spaceLocator(name=f"{self.prefix}_LOC_heel_reverse")

        # ball end reverse
        loc_ball_end_reverse = cmds.spaceLocator(name=f"{self.prefix}_LOC_ball_end_reverse")
        cmds.parent(loc_ball_end_reverse, loc_heel_reverse)
        loc_ball_end_translation = cmds.ls(f"{self.prefix}_LOC_ball_end", type="transform")
        loc_ball_end = cmds.xform(loc_ball_end_translation, query=True, translation=True, worldSpace=True)

        # ball reverse
        loc_ball_reverse = cmds.spaceLocator(name=f"{self.prefix}_LOC_ball_reverse")
        cmds.parent(loc_ball_reverse, loc_ball_end_reverse)
        loc_ball_translation = cmds.ls(f"{self.prefix}_LOC_ball", type="transform")
        loc_ball = cmds.xform(loc_ball_translation, query=True, translation=True, worldSpace=True)

        # ankle reverse
        loc_ankle_reverse = cmds.spaceLocator(name=f"{self.prefix}_LOC_ankle_reverse")
        cmds.parent(loc_ankle_reverse, loc_ball_reverse)
        loc_ankle_translation = cmds.ls(f"{self.prefix}_LOC_ankle", type="transform")
        loc_ankle = cmds.xform(loc_ankle_translation, query=True, translation=True, worldSpace=True)

        # move heel reverse
        cmds.move(loc_ball[0], loc_ball[1], loc_ball[2] - 15, loc_heel_reverse)

        # move ball end reverse
        cmds.move(loc_ball_end[0], loc_ball_end[1], loc_ball_end[2], loc_ball_end_reverse)

        # move ball reverse
        cmds.move(loc_ball[0], loc_ball[1], loc_ball[2], loc_ball_reverse)

        # move ankle reverse
        cmds.move(loc_ankle[0], loc_ankle[1], loc_ankle[2], loc_ankle_reverse)

    def create_foot_roll_joints(self):
        # heel reverse
        # l_def_heel = cmds.ls("L_IK_ball")
        def_heel_reverse_position = cmds.xform(f"{self.prefix}_IK_ball", query=True, translation=True, objectSpace=True)
        def_heel_reverse = cmds.joint(radius=3, name=f"{self.prefix}_DEF_heel_reverse")
        cmds.matchTransform(def_heel_reverse, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)
        cmds.makeIdentity(def_heel_reverse, apply=True, rotate=True)
        cmds.parent(def_heel_reverse, world=True)
        cmds.move(
            0,
            def_heel_reverse_position[1] - 30,
            0,
            def_heel_reverse,
            objectSpace=True,
            relative=True,
        )

        # ball end reverse
        # l_def_ball_end = cmds.ls("L_DEF_ball_end")
        # l_def_ball_end_reverse_position = cmds.xform(l_def_ball_end, query=True, translation=True, worldSpace=True)
        def_ball_end_reverse = cmds.joint(radius=3, name=f"{self.prefix}_DEF_ball_end_reverse")
        cmds.matchTransform(def_ball_end_reverse, f"{self.prefix}_IK_ball_end", position=True, rotation=True,
                            scale=True)
        cmds.makeIdentity(def_ball_end_reverse, apply=True, rotate=True)
        # cmds.parent(l_def_ball_end_reverse, l_def_heel_reverse)

        # ball reverse
        # l_def_ball = cmds.ls("L_DEF_ball")
        # l_def_ball_reverse_position = cmds.xform(l_def_ball, query=True, translation=True, worldSpace=True)
        def_ball_reverse = cmds.joint(radius=3, name=f"{self.prefix}_DEF_ball_reverse")
        cmds.matchTransform(def_ball_reverse, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)
        cmds.makeIdentity(def_ball_reverse, apply=True, rotate=True)
        # cmds.parent(l_def_ball_reverse, l_def_ball_end_reverse)

        # ankle reverse
        # l_def_ankle = cmds.ls("L_DEF_ankle")
        # l_def_ankle_reverse_position = cmds.xform(l_def_ankle, query=True, translation=True, worldSpace=True)
        def_ankle_reverse = cmds.joint(radius=3, name=f"{self.prefix}_DEF_ankle_reverse")
        cmds.matchTransform(def_ankle_reverse, f"{self.prefix}_IK_ankle", position=True, rotation=True, scale=True)
        cmds.makeIdentity(def_ankle_reverse, apply=True, rotate=True)
        # cmds.parent(l_def_ankle_reverse, l_def_ball_reverse)

    def create_foot_roll_handles(self):
        cmds.ikHandle(name=f"{self.prefix}_ikHandle_ball", startJoint=f"{self.prefix}_IK_ankle",
                      endEffector=f"{self.prefix}_IK_ball", solver="ikSCsolver")
        cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_ball_end", startJoint=f"{self.prefix}_IK_ball",
            endEffector=f"{self.prefix}_IK_ball_end", solver="ikSCsolver"
        )

        ik_offset_ball_end = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_ball_end")
        cmds.parent(f"{self.prefix}_IK_OFFSET_ball_end", f"{self.prefix}_DEF_ball_end_reverse")
        cmds.matchTransform(ik_offset_ball_end, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)
        cmds.makeIdentity(ik_offset_ball_end, apply=True, rotate=True)

        cmds.parent(f"{self.prefix}_ikHandle_ball_end", ik_offset_ball_end)

    def create_foot_roll_hierarchy(self):
        ik_offset_foot_roll = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_foot_roll")

        # cmds.parent(l_ik_offset_foot_roll, world=True)
        cmds.parentConstraint(f"{self.prefix}_IK_CTRL_leg", ik_offset_foot_roll, maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_DEF_ankle_reverse", "L_ikHandle_leg", maintainOffset=True)

        # INNER OUTER BANK
        ik_offset_bank = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_bank")
        ik_offset_bank_inner = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_bank_inner")
        ik_offset_bank_outer = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_bank_outer")

        cmds.parent(ik_offset_bank, ik_offset_foot_roll)

        cmds.parent(ik_offset_bank_outer, ik_offset_bank)
        cmds.move(10, 0, 0, ik_offset_bank_outer, localSpace=True, relative=True)

        cmds.parent(ik_offset_bank_inner, ik_offset_bank_outer)
        cmds.move(-10, 0, 0, ik_offset_bank_inner, localSpace=True, relative=True)

        cmds.matchTransform(ik_offset_bank, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)

        # cmds.matchTransform(ik_offset_bank_inner, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)
        cmds.makeIdentity(ik_offset_bank_inner, apply=True, rotate=False, translate=True)

        # cmds.matchTransform(ik_offset_bank_outer, f"{self.prefix}_IK_ball", position=True, rotation=True, scale=True)
        cmds.makeIdentity(ik_offset_bank_outer, apply=True, rotate=False, translate=True)

        cmds.parent(f"{self.prefix}_DEF_heel_reverse", ik_offset_bank_inner)

        cmds.parent(f"{self.prefix}_ikHandle_ball", f"{self.prefix}_DEF_ball_reverse")

    def create_foot_roll_attributes(self):
        # Bank
        if not cmds.attributeQuery("Bank", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg", attributeType="float", niceName="Bank", longName="Bank", defaultValue=0,
                minValue=-30, maxValue=30, keyable=True
            )

        # Twist
        if not cmds.attributeQuery("Heel_Twist", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Heel Twist",
                longName="Heel_Twist",
                defaultValue=0,
                minValue=-30,
                maxValue=30,
                keyable=True,
            )

        # Toe
        if not cmds.attributeQuery("Toe_Tap", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Toe Tap",
                longName="Toe_Tap",
                defaultValue=0,
                minValue=-30,
                maxValue=30,
                keyable=True,
            )

        if not cmds.attributeQuery("Toe_Twist", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Toe Twist",
                longName="Toe_Twist",
                defaultValue=0,
                minValue=-30,
                maxValue=30,
                keyable=True,
            )

        if not cmds.attributeQuery("Toe_Snap", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Toe Snap",
                longName="Toe_Snap",
                defaultValue=5,
                minValue=0,
                maxValue=10,
                keyable=True,
            )

        # Roll
        if not cmds.attributeQuery("Roll", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg", attributeType="float", niceName="Roll", longName="Roll", defaultValue=0,
                minValue=-10, maxValue=10, keyable=True
            )

        if not cmds.attributeQuery("Roll_Back", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Roll Back",
                longName="Roll_Back",
                defaultValue=5,
                minValue=0,
                maxValue=5,
                keyable=True,
            )

        if not cmds.attributeQuery("Roll_End", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Roll End",
                longName="Roll_End",
                defaultValue=10,
                minValue=0,
                maxValue=10,
                keyable=True,
            )

    def create_foot_roll_nodes(self):
        foot_bank_condition_node = cmds.createNode("condition", name=f"{self.prefix}_foot_bank_condition")
        cmds.setAttr(f"{foot_bank_condition_node}.operation", CONOperation.GREATER_OR_EQUAL.value)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Bank", f"{foot_bank_condition_node}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Bank", f"{foot_bank_condition_node}.colorIfFalse.colorIfFalseG")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Bank", f"{foot_bank_condition_node}.firstTerm")

        cmds.connectAttr(f"{foot_bank_condition_node}.outColor.outColorR",
                         f"{self.prefix}_IK_OFFSET_bank_inner.rotate.rotateY")
        cmds.connectAttr(f"{foot_bank_condition_node}.outColor.outColorG",
                         f"{self.prefix}_IK_OFFSET_bank_outer.rotate.rotateY")

        self.create_foot_roll_ball_end_node()
        self.create_foot_roll_ball_node()
        self.create_foot_roll_heel_node()
        self.create_toe_tap_node()

    def create_foot_roll_ball_end_node(self):
        ball_end_reverse_condition_node = cmds.createNode("condition", name=f"{self.prefix}_ball_end_reverse_condition")
        cmds.setAttr(f"{ball_end_reverse_condition_node}.operation", CONOperation.GREATER_OR_EQUAL.value)
        cmds.setAttr(f"{ball_end_reverse_condition_node}.colorIfFalseR", 0)

        ball_end_reverse_plus_minus_average_node = cmds.createNode("plusMinusAverage",
                                                                   name=f"{self.prefix}_bank_reverse_plus_minus_average")
        cmds.setAttr(f"{ball_end_reverse_plus_minus_average_node}.operation", PMAOperation.SUBTRACT.value)

        ball_end_reverse_multiply_divide_node = cmds.createNode("multiplyDivide",
                                                                name=f"{self.prefix}_bank_reverse_multiply_divide")
        cmds.setAttr(f"{ball_end_reverse_multiply_divide_node}.operation", MUDOperation.MULTIPLY.value)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{ball_end_reverse_plus_minus_average_node}.input1D[0]")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Toe_Snap",
                         f"{ball_end_reverse_plus_minus_average_node}.input1D[1]")

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{ball_end_reverse_condition_node}.firstTerm")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Toe_Snap", f"{ball_end_reverse_condition_node}.secondTerm")

        cmds.connectAttr(f"{ball_end_reverse_plus_minus_average_node}.output1D",
                         f"{ball_end_reverse_condition_node}.colorIfTrue.colorIfTrueR")

        cmds.connectAttr(f"{ball_end_reverse_condition_node}.outColor.outColorR",
                         f"{ball_end_reverse_multiply_divide_node}.input1.input1X")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll_End",
                         f"{ball_end_reverse_multiply_divide_node}.input2.input2X")

        cmds.connectAttr(f"{ball_end_reverse_multiply_divide_node}.output.outputX",
                         f"{self.prefix}_DEF_ball_end_reverse.rotate.rotateX")

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Toe_Twist", f"{self.prefix}_DEF_ball_end_reverse.rotate.rotateZ")

    def create_toe_twist_node(self):
        pass

    def create_toe_tap_node(self):
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Toe_Tap", f"{self.prefix}_IK_OFFSET_ball_end.rotateX")

    def create_foot_roll_ball_node(self):
        ball_reverse_condition_node = cmds.createNode("condition", name=f"{self.prefix}_DEF_ball_reverse_condition")
        cmds.setAttr(f"{ball_reverse_condition_node}.operation", CONOperation.GREATER_OR_EQUAL.value)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{ball_reverse_condition_node}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{ball_reverse_condition_node}.firstTerm")

        cmds.connectAttr(f"{ball_reverse_condition_node}.outColor.outColorR",
                         f"{self.prefix}_DEF_ball_reverse.rotate.rotateX")

    def create_foot_roll_heel_node(self):
        heel_reverse_condition_node = cmds.createNode("condition", name=f"{self.prefix}_DEF_heel_reverse_condition")
        cmds.setAttr(f"{heel_reverse_condition_node}.operation", CONOperation.LESS_THAN.value)
        cmds.setAttr(f"{heel_reverse_condition_node}.colorIfFalseR", 0)

        heel_reverse_multiply_divide_node = cmds.createNode("multiplyDivide",
                                                            name=f"{self.prefix}_heel_reverse_multiply_divide")
        cmds.setAttr(f"{heel_reverse_multiply_divide_node}.operation", MUDOperation.MULTIPLY.value)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{heel_reverse_condition_node}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll", f"{heel_reverse_condition_node}.firstTerm")
        cmds.connectAttr(f"{heel_reverse_condition_node}.outColorR",
                         f"{heel_reverse_multiply_divide_node}.input1.input1X")

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Roll_Back", f"{heel_reverse_multiply_divide_node}.input2.input2X")

        cmds.connectAttr(f"{heel_reverse_multiply_divide_node}.output.outputX",
                         f"{self.prefix}_DEF_heel_reverse.rotate.rotateX")

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Heel_Twist", f"{self.prefix}_DEF_heel_reverse.rotate.rotateZ")
