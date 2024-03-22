import maya.cmds as cmds
from utilities.enums import MUDOperation, Stretch


class ArmStretch:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_arm_stretch_nodes(self):
        # DISTANCE BETWEEN NODES
        upperarm_to_lowerarm_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_upperarm_stretch.worldMatrix[0]",
                         f"{upperarm_to_lowerarm_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_lowerarm_stretch.worldMatrix[0]",
                         f"{upperarm_to_lowerarm_distance}.inMatrix2")

        lowerarm_to_wrist_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_lowerarm_stretch.worldMatrix[0]",
                         f"{lowerarm_to_wrist_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_wrist_stretch.worldMatrix[0]", f"{lowerarm_to_wrist_distance}.inMatrix2")

        upperarm_to_ik_ctrl_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_upperarm_stretch.worldMatrix[0]",
                         f"{upperarm_to_ik_ctrl_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_LOC_arm_stretch_end.worldMatrix[0]",
                         f"{upperarm_to_ik_ctrl_distance}.inMatrix2")

        # ADD DOUBLE LINEAR NODE
        total_arm_length = cmds.createNode("addDoubleLinear")
        cmds.connectAttr(f"{upperarm_to_lowerarm_distance}.distance", f"{total_arm_length}.input1")
        cmds.connectAttr(f"{lowerarm_to_wrist_distance}.distance", f"{total_arm_length}.input2")

        # CONDITION NODES
        arm_stretch_condition = cmds.createNode("condition", name=f"{self.prefix}_arm_stretch_condition")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_arm.Stretch_Type", f"{arm_stretch_condition}.operation")
        cmds.connectAttr(f"{upperarm_to_ik_ctrl_distance}.distance", f"{arm_stretch_condition}.firstTerm")
        cmds.connectAttr(f"{total_arm_length}.output", f"{arm_stretch_condition}.secondTerm")

        # MULTIPLY DIVIDE NODE
        arm_scale_factor = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{arm_scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{upperarm_to_ik_ctrl_distance}.distance", f"{arm_scale_factor}.input1.input1X")
        cmds.connectAttr(f"{total_arm_length}.output", f"{arm_scale_factor}.input2.input2X")

        # BLEND COLOR NODES
        color_attributes = ["R", "G", "B"]

        arm_stretch_ik_blend = cmds.createNode("blendColors", name=f"{self.prefix}_arm_stretch_ik_blend")
        for color_attribute in color_attributes:
            cmds.setAttr(f"{arm_stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{arm_stretch_ik_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_arm.IK_FK_SWITCH", f"{arm_stretch_ik_blend}.blender")

        arm_stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_arm_stretch_blend")
        for color_attribute in color_attributes:
            cmds.setAttr(f"{arm_stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{arm_stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_arm.Stretchiness", f"{arm_stretch_blend}.blender")

        cmds.connectAttr(f"{arm_scale_factor}.output.outputX", f"{arm_stretch_blend}.color1.color1R")
        cmds.connectAttr(f"{arm_stretch_blend}.output.outputR", f"{arm_stretch_condition}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{arm_stretch_condition}.outColor.outColorR", f"{arm_stretch_ik_blend}.color1.color1R")

        # POSITION VOLUME NODES
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_IK_upperarm.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_IK_lowerarm.scale.scaleY")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_DEF_lowerarm.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_DEF_wrist.scale.scaleY")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR",
                         f"{self.prefix}_MCH_upperarm_roll_start.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_upperarm_roll_end.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleY")

        # PRESERVE VOLUME NODES
        arm_volume_preservation = cmds.createNode("multiplyDivide", name=f"{self.prefix}_arm_volume_preservation")
        cmds.setAttr(f"{arm_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.setAttr(f"{arm_volume_preservation}.input2.input2X", -1)
        cmds.connectAttr(f"{arm_stretch_condition}.outColor.outColorR", f"{arm_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{arm_volume_preservation}.output.outputX", f"{arm_stretch_ik_blend}.color1.color1G")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_lowerarm.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_lowerarm.scale.scaleZ")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_wrist.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_wrist.scale.scaleZ")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG",
                         f"{self.prefix}_MCH_upperarm_roll_start.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG",
                         f"{self.prefix}_MCH_upperarm_roll_start.scale.scaleZ")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_upperarm_roll_end.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_upperarm_roll_end.scale.scaleZ")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleZ")

    def create_arm_stretch_locators(self):
        loc_arm_stretch_end = cmds.spaceLocator(name=f"{self.prefix}_LOC_arm_stretch_end")
        # cmds.matchTransform(l_loc_arm_stretch_end, "L_IK_CTRL_arm", position=True, rotation=True, scale=False)
        constraint = cmds.parentConstraint(f"{self.prefix}_IK_CTRL_arm", loc_arm_stretch_end)
        cmds.delete(constraint)
        cmds.parent(loc_arm_stretch_end, f"{self.prefix}_IK_CTRL_arm")

    def create_arm_stretch_joints(self):
        mch_upperarm_stretch = cmds.duplicate(f"{self.prefix}_DEF_upperarm", parentOnly=True,
                                              name=f"{self.prefix}_MCH_upperarm_stretch")
        mch_lowerarm_stretch = cmds.duplicate(f"{self.prefix}_DEF_lowerarm", parentOnly=True,
                                              name=f"{self.prefix}_MCH_lowerarm_stretch")
        mch_wrist_stretch = cmds.duplicate(f"{self.prefix}_DEF_wrist", parentOnly=True,
                                           name=f"{self.prefix}_MCH_wrist_stretch")

        cmds.parent(mch_upperarm_stretch, "rig_systems")
        cmds.parent(mch_lowerarm_stretch, mch_upperarm_stretch)
        cmds.parent(mch_wrist_stretch, mch_lowerarm_stretch)

    def create_arm_stretch_attributes(self):
        # CATEGORY STRETCH
        if not cmds.attributeQuery("STRETCH", node=f"{self.prefix}_IK_CTRL_arm", exists=True):
            cmds.addAttr(f"{self.prefix}_IK_CTRL_arm", attributeType="enum", niceName="STRETCH", longName="STRETCH",
                         enumName="---------")
            cmds.setAttr(f"{self.prefix}_IK_CTRL_arm.STRETCH", keyable=False, lock=True, channelBox=True)

        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node=f"{self.prefix}_IK_CTRL_arm", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_arm",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node=f"{self.prefix}_IK_CTRL_arm", exists=True):
            cmds.addAttr(f"{self.prefix}_IK_CTRL_arm",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=Stretch.STRETCH.value,
                         enumName=f"{Stretch.BOTH.name}={Stretch.BOTH.value}:{Stretch.STRETCH.name}={Stretch.STRETCH.value}:{Stretch.SQUASH.name}={Stretch.SQUASH.value}",
                         keyable=True,
                         )
