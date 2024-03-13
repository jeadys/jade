import maya.cmds as cmds
from utilities.enums import MUDOperation, Stretch


class LegStretch:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_leg_stretch_nodes(self):
        # DISTANCE BETWEEN NODES
        upperleg_to_lowerleg_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_upperleg_stretch.worldMatrix[0]",
                         f"{upperleg_to_lowerleg_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_lowerleg_stretch.worldMatrix[0]",
                         f"{upperleg_to_lowerleg_distance}.inMatrix2")

        lowerleg_to_ankle_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_lowerleg_stretch.worldMatrix[0]",
                         f"{lowerleg_to_ankle_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_ankle_stretch.worldMatrix[0]", f"{lowerleg_to_ankle_distance}.inMatrix2")

        upperleg_to_ik_ctrl_distance = cmds.createNode("distanceBetween")
        cmds.connectAttr(f"{self.prefix}_MCH_upperleg_stretch.worldMatrix[0]",
                         f"{upperleg_to_ik_ctrl_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_LOC_leg_stretch_end.worldMatrix[0]",
                         f"{upperleg_to_ik_ctrl_distance}.inMatrix2")

        # ADD DOUBLE LINEAR NODE
        total_leg_length = cmds.createNode("addDoubleLinear")
        cmds.connectAttr(f"{upperleg_to_lowerleg_distance}.distance", f"{total_leg_length}.input1")
        cmds.connectAttr(f"{lowerleg_to_ankle_distance}.distance", f"{total_leg_length}.input2")

        # CONDITION NODES
        leg_stretch_condition = cmds.createNode("condition", name=f"{self.prefix}_leg_stretch_condition")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Stretch_Type", f"{leg_stretch_condition}.operation")
        cmds.connectAttr(f"{upperleg_to_ik_ctrl_distance}.distance", f"{leg_stretch_condition}.firstTerm")
        cmds.connectAttr(f"{total_leg_length}.output", f"{leg_stretch_condition}.secondTerm")

        # MULTIPLY DIVIDE NODE
        leg_scale_factor = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{leg_scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{upperleg_to_ik_ctrl_distance}.distance", f"{leg_scale_factor}.input1.input1X")
        cmds.connectAttr(f"{total_leg_length}.output", f"{leg_scale_factor}.input2.input2X")

        # BLEND COLOR NODES
        color_attributes = ["R", "G", "B"]

        leg_stretch_ik_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_ik_blend")
        for color_attribute in color_attributes:
            cmds.setAttr(f"{leg_stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{leg_stretch_ik_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.IK_FK_SWITCH", f"{leg_stretch_ik_blend}.blender")

        leg_stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_blend")
        for color_attribute in color_attributes:
            cmds.setAttr(f"{leg_stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{leg_stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Stretchiness", f"{leg_stretch_blend}.blender")

        cmds.connectAttr(f"{leg_scale_factor}.output.outputX", f"{leg_stretch_blend}.color1.color1R")
        cmds.connectAttr(f"{leg_stretch_blend}.output.outputR", f"{leg_stretch_condition}.colorIfTrue.colorIfTrueR")
        cmds.connectAttr(f"{leg_stretch_condition}.outColor.outColorR", f"{leg_stretch_ik_blend}.color1.color1R")

        # POSITION VOLUME NODES
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_IK_upperleg.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_IK_lowerleg.scale.scaleY")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_DEF_lowerleg.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_DEF_ankle.scale.scaleY")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR",
                         f"{self.prefix}_MCH_upperleg_roll_start.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_upperleg_roll_end.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleY")

        # PRESERVE VOLUME NODES
        leg_volume_preservation = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_volume_preservation")
        cmds.setAttr(f"{leg_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.setAttr(f"{leg_volume_preservation}.input2.input2X", -1)
        cmds.connectAttr(f"{leg_stretch_condition}.outColor.outColorR", f"{leg_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{leg_volume_preservation}.output.outputX", f"{leg_stretch_ik_blend}.color1.color1G")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_lowerleg.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_lowerleg.scale.scaleZ")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_ankle.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_ankle.scale.scaleZ")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG",
                         f"{self.prefix}_MCH_upperleg_roll_start.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG",
                         f"{self.prefix}_MCH_upperleg_roll_start.scale.scaleZ")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_upperleg_roll_end.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_upperleg_roll_end.scale.scaleZ")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleZ")

    def create_leg_stretch_locators(self):
        loc_leg_stretch_end = cmds.spaceLocator(name=f"{self.prefix}_LOC_leg_stretch_end")
        # cmds.matchTransform(l_loc_leg_stretch_end, "L_IK_CTRL_leg", position=True, rotation=True, scale=False)
        constraint = cmds.parentConstraint(f"{self.prefix}_IK_CTRL_leg", loc_leg_stretch_end)
        cmds.delete(constraint)
        cmds.parent(loc_leg_stretch_end, f"{self.prefix}_IK_CTRL_leg")

    def create_leg_stretch_joints(self):
        mch_upperleg_stretch = cmds.duplicate(f"{self.prefix}_DEF_upperleg", parentOnly=True,
                                              name=f"{self.prefix}_MCH_upperleg_stretch")
        mch_lowerleg_stretch = cmds.duplicate(f"{self.prefix}_DEF_lowerleg", parentOnly=True,
                                              name=f"{self.prefix}_MCH_lowerleg_stretch")
        mch_ankle_stretch = cmds.duplicate(f"{self.prefix}_DEF_ankle", parentOnly=True,
                                           name=f"{self.prefix}_MCH_ankle_stretch")

        cmds.parent(mch_upperleg_stretch, "rig_systems")
        cmds.parent(mch_lowerleg_stretch, mch_upperleg_stretch)
        cmds.parent(mch_ankle_stretch, mch_lowerleg_stretch)

    def create_arm_stretch_attributes(self):
        # CATEGORY STRETCH
        if not cmds.attributeQuery("STRETCH", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(f"{self.prefix}_IK_CTRL_leg", attributeType="enum", niceName="STRETCH", longName="STRETCH",
                         enumName="---------")
            cmds.setAttr(f"{self.prefix}_IK_CTRL_leg.STRETCH", keyable=False, lock=True, channelBox=True)

        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(
                f"{self.prefix}_IK_CTRL_leg",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node=f"{self.prefix}_IK_CTRL_leg", exists=True):
            cmds.addAttr(f"{self.prefix}_IK_CTRL_leg",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=Stretch.STRETCH.value,
                         enumName=f"{Stretch.BOTH.name}={Stretch.BOTH.value}:{Stretch.STRETCH.name}={Stretch.STRETCH.value}:{Stretch.SQUASH.name}={Stretch.SQUASH.value}",
                         keyable=True,
                         )
