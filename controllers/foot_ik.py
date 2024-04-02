import maya.cmds as cmds
from dataclasses import dataclass
from utilities.enums import CONOperation


@dataclass(frozen=True)
class FootSegment:
    name: str
    position: tuple[float, float, float]


class FootIK:
    locator_parent_group = "locators"
    joint_parent_group = "skeleton"

    def __init__(self, prefix, rotation_order):
        self.prefix = prefix
        self.rotation_order = rotation_order
        self.foot_segments = [f"{self.prefix}_bank_r_RF", f"{self.prefix}_bank_l_RF", f"{self.prefix}_heel_RF",
                              f"{self.prefix}_pivot_RF", f"{self.prefix}_toe_RF", f"{self.prefix}_ball_RF",
                              f"{self.prefix}_ankle_RF"]

    def create_foot_ik(self):
        self.create_ik_foot_controls()
        self.create_foot_bank()
        self.create_foot_roll()
        self.create_foot_heel()
        self.create_foot_toe()

    def create_ik_foot_controls(self):
        scik_ankle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_ankle",
            startJoint=f"{self.prefix}_ankle_IK",
            endEffector=f"{self.prefix}_ball_IK",
            solver="ikSCsolver")[0]

        scik_ball = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_ball",
            startJoint=f"{self.prefix}_ball_IK",
            endEffector=f"{self.prefix}_toe_IK",
            solver="ikSCsolver")[0]

        cmds.parent(f"{self.prefix}_ikHandle_leg", f"{self.prefix}_ankle_RF")
        cmds.parent(scik_ankle, f"{self.prefix}_ball_RF")
        cmds.parent(scik_ball, f"{self.prefix}_toe_RF")
        cmds.parent(self.foot_segments[0], f"{self.prefix}_leg_IK_CTRL")

    def create_foot_bank(self):
        if not cmds.attributeQuery("Bank", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_leg_IK_CTRL", attributeType="float", niceName="Bank", longName="Bank",
                         defaultValue=0, minValue=-30, maxValue=30, keyable=True)

        foot_bank_condition_node = cmds.createNode("condition", name=f"{self.prefix}_foot_bank_condition")
        cmds.setAttr(f"{foot_bank_condition_node}.operation", CONOperation.GREATER_OR_EQUAL.value)

        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Bank", f"{foot_bank_condition_node}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Bank", f"{foot_bank_condition_node}.colorIfFalse.colorIfFalseG")
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Bank", f"{foot_bank_condition_node}.firstTerm")

        cmds.connectAttr(f"{foot_bank_condition_node}.outColor.outColorR",
                         f"{self.prefix}_bank_r_RF.rotate.rotateZ")
        cmds.connectAttr(f"{foot_bank_condition_node}.outColor.outColorG",
                         f"{self.prefix}_bank_l_RF.rotate.rotateZ")

    def create_foot_roll(self):
        if not cmds.attributeQuery("Roll", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_leg_IK_CTRL", attributeType="float", niceName="Roll", longName="Roll",
                         defaultValue=0, minValue=-30, maxValue=30, keyable=True)

        foot_roll_condition_node = cmds.createNode("condition", name=f"{self.prefix}_foot_roll_condition")
        cmds.setAttr(f"{foot_roll_condition_node}.operation", CONOperation.GREATER_OR_EQUAL.value)

        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Roll", f"{foot_roll_condition_node}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Roll", f"{foot_roll_condition_node}.colorIfFalse.colorIfFalseG")
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Roll", f"{foot_roll_condition_node}.firstTerm")

        cmds.connectAttr(f"{foot_roll_condition_node}.outColor.outColorR",
                         f"{self.prefix}_heel_RF.rotate.rotateZ")
        cmds.connectAttr(f"{foot_roll_condition_node}.outColor.outColorG",
                         f"{self.prefix}_toe_RF.rotate.rotateZ")

    def create_foot_heel(self):
        if not cmds.attributeQuery("Heel", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_leg_IK_CTRL", attributeType="float", niceName="Heel", longName="Heel",
                         defaultValue=0, minValue=-30, maxValue=30, keyable=True)

        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Heel", f"{self.prefix}_heel_RF.rotate.rotateX")

    def create_foot_toe(self):
        if not cmds.attributeQuery("Toe", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_leg_IK_CTRL", attributeType="float", niceName="Toe", longName="Toe",
                         defaultValue=0, minValue=-30, maxValue=30, keyable=True)

        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Toe", f"{self.prefix}_toe_RF.rotate.rotateX")