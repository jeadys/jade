import maya.cmds as cmds

from utilities.enums import CONOperation, MUDOperation
from enum import Enum


class Stretch(Enum):
    BOTH = 1
    STRETCH = 3
    SQUASH = 5


class LegStretch:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_leg_stretch_locators(self):
        loc_leg_stretch_end = cmds.spaceLocator(name=f"{self.prefix}_LOC_leg_stretch_end")
        # cmds.matchTransform(l_loc_leg_stretch_end, "L_IK_CTRL_leg", position=True, rotation=True, scale=False)
        constraint = cmds.parentConstraint(f"{self.prefix}_IK_CTRL_leg", loc_leg_stretch_end)
        cmds.delete(constraint)
        cmds.parent(loc_leg_stretch_end, f"{self.prefix}_IK_CTRL_leg")

    def create_leg_stretch_joints(self):
        mch_femur_stretch = cmds.duplicate(f"{self.prefix}_DEF_femur", parentOnly=True,
                                           name=f"{self.prefix}_MCH_femur_stretch")
        mch_tibia_stretch = cmds.duplicate(f"{self.prefix}_DEF_tibia", parentOnly=True,
                                           name=f"{self.prefix}_MCH_tibia_stretch")
        mch_ankle_stretch = cmds.duplicate(f"{self.prefix}_DEF_ankle", parentOnly=True,
                                           name=f"{self.prefix}_MCH_ankle_stretch")

        cmds.parent(mch_femur_stretch, "rig_systems")
        cmds.parent(mch_tibia_stretch, mch_femur_stretch)
        cmds.parent(mch_ankle_stretch, mch_tibia_stretch)

    def create_leg_stretch_nodes(self):
        # DISTANCE BETWEEN FEMUR STRETCH - TIBIA STRETCH
        femur_stretch_length = cmds.createNode("distanceBetween", name="femur_stretch_length")

        cmds.connectAttr(f"{self.prefix}_MCH_femur_stretch.worldMatrix[0]", f"{femur_stretch_length}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_tibia_stretch.worldMatrix[0]", f"{femur_stretch_length}.inMatrix2")

        # DISTANCE BETWEEN TIBIA STRETCH - ANKLE STRETCH
        tibia_stretch_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_tibia_stretch_length")

        cmds.connectAttr(f"{self.prefix}_MCH_tibia_stretch.worldMatrix[0]", f"{tibia_stretch_length}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_ankle_stretch.worldMatrix[0]", f"{tibia_stretch_length}.inMatrix2")

        # TOTAL LENGTH OF LEG
        leg_length = cmds.createNode("addDoubleLinear", name=f"{self.prefix}_leg_length")

        cmds.connectAttr(f"{femur_stretch_length}.distance", f"{leg_length}.input1")
        cmds.connectAttr(f"{tibia_stretch_length}.distance", f"{leg_length}.input2")

        # DISTANCE BETWEEN FEMUR STRETCH - IK CONTROLLER POSITION
        leg_ik_distance = cmds.createNode("distanceBetween", name="l_leg_ik_distance")

        cmds.connectAttr(f"{self.prefix}_MCH_femur_stretch.worldMatrix[0]", f"{leg_ik_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_LOC_leg_stretch_end.worldMatrix[0]", f"{leg_ik_distance}.inMatrix2")

        # CHECK WHEN JOINT NEEDS TO STRETCH
        leg_stretch_condition = cmds.createNode("condition", name=f"{self.prefix}_leg_stretch_condition")

        # Determines if arm should SQUASH, STRETCH or BOTH
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Stretch_Type", f"{leg_stretch_condition}.operation")

        cmds.connectAttr(f"{leg_ik_distance}.distance", f"{leg_stretch_condition}.firstTerm")
        cmds.connectAttr(f"{leg_length}.output", f"{leg_stretch_condition}.secondTerm")

        # CORRECT SCALING WHEN JOINT IS STRETCHED
        leg_scale_multiply = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_scale_multiply")
        cmds.setAttr(f"{leg_scale_multiply}.operation", MUDOperation.DIVIDE.value)

        cmds.connectAttr(f"{leg_ik_distance}.distance", f"{leg_scale_multiply}.input1.input1X")
        cmds.connectAttr(f"{leg_length}.output", f"{leg_scale_multiply}.input2.input2X")

        cmds.connectAttr(f"{leg_scale_multiply}.output.outputX", f"{leg_stretch_condition}.colorIfTrue.colorIfTrueR")

        # SCALE AND POSITION ROLL JOINTS
        leg_roll_scale_multiply = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_roll_scale_multiply")
        cmds.setAttr(f"{leg_roll_scale_multiply}.operation", MUDOperation.MULTIPLY.value)
        if cmds.objExists(f"{self.prefix}_MCH_thigh_roll_end"):
            # DISTANCE BETWEEN FEMUR - TIBIA
            femur_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_femur_length")

            cmds.connectAttr(f"{self.prefix}_DEF_femur.worldMatrix[0]", f"{femur_length}.inMatrix1")
            cmds.connectAttr(f"{self.prefix}_DEF_tibia.worldMatrix[0]", f"{femur_length}.inMatrix2")

            # POSITION ROLL JOINTS
            cmds.setAttr(f"{leg_roll_scale_multiply}.input2.input2X", 0.5)
            cmds.connectAttr(f"{femur_length}.distance", f"{leg_roll_scale_multiply}.input1.input1X")
            cmds.connectAttr(f"{leg_roll_scale_multiply}.output.outputX",
                             f"{self.prefix}_MCH_thigh_roll_end.translate.translateY")

        if cmds.objExists(f"{self.prefix}_MCH_ankle_roll_end"):
            # DISTANCE BETWEEN TIBIA - ANKLE
            tibia_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_tibia_length")

            cmds.connectAttr(f"{self.prefix}_DEF_tibia.worldMatrix[0]", f"{tibia_length}.inMatrix1")
            cmds.connectAttr(f"{self.prefix}_DEF_ankle.worldMatrix[0]", f"{tibia_length}.inMatrix2")

            # POSITION ROLL JOINTS
            cmds.setAttr(f"{leg_roll_scale_multiply}.input2.input2Y", 0.5)
            cmds.connectAttr(f"{tibia_length}.distance", f"{leg_roll_scale_multiply}.input1.input1Y")
            cmds.connectAttr(f"{leg_roll_scale_multiply}.output.outputY",
                             f"{self.prefix}_MCH_ankle_roll_end.translate.translateY")

        # STRETCH ONLY IN IK AND DISABLE IT IN FK MODE
        # SCALE ROLL JOINTS
        leg_stretch_ik_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_ik_blend")
        cmds.setAttr(f"{leg_stretch_ik_blend}.color1R", 1)
        cmds.setAttr(f"{leg_stretch_ik_blend}.color1G", 1)
        cmds.setAttr(f"{leg_stretch_ik_blend}.color1B", 1)
        cmds.setAttr(f"{leg_stretch_ik_blend}.color2R", 1)
        cmds.setAttr(f"{leg_stretch_ik_blend}.color2G", 1)
        cmds.setAttr(f"{leg_stretch_ik_blend}.color2B", 1)

        cmds.connectAttr(f"{self.prefix}_SWITCH_CTRL_leg.IK_FK_SWITCH", f"{leg_stretch_ik_blend}.blender")
        cmds.connectAttr(f"{leg_stretch_condition}.outColor.outColorR", f"{leg_stretch_ik_blend}.color1.color1R")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_thigh_roll_end.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleY")

        # BLEND BETWEEN STRETCH AND NON STRETCH
        leg_stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_blend")
        cmds.setAttr(f"{leg_stretch_blend}.color1R", 1)
        cmds.setAttr(f"{leg_stretch_blend}.color1G", 1)
        cmds.setAttr(f"{leg_stretch_blend}.color1B", 1)
        cmds.setAttr(f"{leg_stretch_blend}.color2R", 1)
        cmds.setAttr(f"{leg_stretch_blend}.color2G", 1)
        cmds.setAttr(f"{leg_stretch_blend}.color2B", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_leg.Stretchiness", f"{leg_stretch_blend}.blender")
        # SCALE IK LEG JOINTS
        cmds.connectAttr(f"{leg_stretch_condition}.outColor.outColorR", f"{leg_stretch_blend}.color1.color1R")
        cmds.connectAttr(f"{leg_stretch_blend}.output.outputR", f"{self.prefix}_IK_femur.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_blend}.output.outputR", f"{self.prefix}_IK_tibia.scale.scaleY")

        # Preserve volume of mesh on stretch
        leg_volume_preservation = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_volume_preservation")
        cmds.setAttr(f"{leg_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.setAttr(f"{leg_volume_preservation}.input2.input2X", -1)
        cmds.connectAttr(f"{leg_stretch_condition}.outColor.outColorR", f"{leg_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{leg_volume_preservation}.output.outputX", f"{leg_stretch_ik_blend}.color1.color1G")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_femur.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_femur.scale.scaleZ")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_tibia.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_tibia.scale.scaleZ")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_thigh_roll_end.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_thigh_roll_end.scale.scaleZ")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_ankle_roll_end.scale.scaleZ")

    def create_leg_stretch_attributes(self):
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
