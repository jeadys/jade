import maya.cmds as cmds

from utilities.enums import CONOperation, MUDOperation
from enum import Enum


class Stretch(Enum):
    BOTH = 1
    STRETCH = 3
    SQUASH = 5


class ArmStretch:

    def __init__(self, prefix):
        self.prefix = prefix

    def create_arm_stretch_locators(self):
        loc_arm_stretch_end = cmds.spaceLocator(name=f"{self.prefix}_LOC_arm_stretch_end")
        # cmds.matchTransform(l_loc_arm_stretch_end, "L_IK_CTRL_arm", position=True, rotation=True, scale=False)
        constraint = cmds.parentConstraint(f"{self.prefix}_IK_CTRL_arm", loc_arm_stretch_end)
        cmds.delete(constraint)
        cmds.parent(loc_arm_stretch_end, f"{self.prefix}_IK_CTRL_arm")

    def create_arm_stretch_joints(self):
        mch_humerus_stretch = cmds.duplicate(f"{self.prefix}_DEF_humerus", parentOnly=True,
                                             name=f"{self.prefix}_MCH_humerus_stretch")
        mch_radius_stretch = cmds.duplicate(f"{self.prefix}_DEF_radius", parentOnly=True,
                                            name=f"{self.prefix}_MCH_radius_stretch")
        mch_wrist_stretch = cmds.duplicate(f"{self.prefix}_DEF_wrist", parentOnly=True,
                                           name=f"{self.prefix}_MCH_wrist_stretch")

        cmds.parent(mch_humerus_stretch, "rig_systems")
        cmds.parent(mch_radius_stretch, mch_humerus_stretch)
        cmds.parent(mch_wrist_stretch, mch_radius_stretch)

    def create_arm_stretch_nodes(self):
        # DISTANCE BETWEEN humerus STRETCH - radius STRETCH
        humerus_stretch_length = cmds.createNode("distanceBetween", name="humerus_stretch_length")

        cmds.connectAttr(f"{self.prefix}_MCH_humerus_stretch.worldMatrix[0]", f"{humerus_stretch_length}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_radius_stretch.worldMatrix[0]", f"{humerus_stretch_length}.inMatrix2")

        # DISTANCE BETWEEN radius STRETCH - WRIST STRETCH
        radius_stretch_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_radius_stretch_length")

        cmds.connectAttr(f"{self.prefix}_MCH_radius_stretch.worldMatrix[0]", f"{radius_stretch_length}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_MCH_wrist_stretch.worldMatrix[0]", f"{radius_stretch_length}.inMatrix2")

        # TOTAL LENGTH OF Arm
        arm_length = cmds.createNode("addDoubleLinear", name=f"{self.prefix}_arm_length")

        cmds.connectAttr(f"{humerus_stretch_length}.distance", f"{arm_length}.input1")
        cmds.connectAttr(f"{radius_stretch_length}.distance", f"{arm_length}.input2")

        # DISTANCE BETWEEN HUMERUS STRETCH - IK CONTROLLER POSITION
        arm_ik_distance = cmds.createNode("distanceBetween", name="l_arm_ik_distance")

        cmds.connectAttr(f"{self.prefix}_MCH_humerus_stretch.worldMatrix[0]", f"{arm_ik_distance}.inMatrix1")
        cmds.connectAttr(f"{self.prefix}_LOC_arm_stretch_end.worldMatrix[0]", f"{arm_ik_distance}.inMatrix2")

        # CHECK WHEN JOINT NEEDS TO STRETCH
        arm_stretch_condition = cmds.createNode("condition", name=f"{self.prefix}_arm_stretch_condition")

        # Determines if arm should SQUASH, STRETCH or BOTH
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_arm.Stretch_Type", f"{arm_stretch_condition}.operation")

        cmds.connectAttr(f"{arm_ik_distance}.distance", f"{arm_stretch_condition}.firstTerm")
        cmds.connectAttr(f"{arm_length}.output", f"{arm_stretch_condition}.secondTerm")

        # CORRECT SCALING WHEN JOINT IS STRETCHED
        arm_scale_multiply = cmds.createNode("multiplyDivide", name=f"{self.prefix}_arm_scale_multiply")
        cmds.setAttr(f"{arm_scale_multiply}.operation", MUDOperation.DIVIDE.value)

        cmds.connectAttr(f"{arm_ik_distance}.distance", f"{arm_scale_multiply}.input1.input1X")
        cmds.connectAttr(f"{arm_length}.output", f"{arm_scale_multiply}.input2.input2X")

        cmds.connectAttr(f"{arm_scale_multiply}.output.outputX", f"{arm_stretch_condition}.colorIfTrue.colorIfTrueR")

        # SCALE AND POSITION ROLL JOINTS
        arm_roll_scale_multiply = cmds.createNode("multiplyDivide", name=f"{self.prefix}_arm_roll_scale_multiply")
        cmds.setAttr(f"{arm_roll_scale_multiply}.operation", MUDOperation.MULTIPLY.value)
        if cmds.objExists(f"{self.prefix}_MCH_shoulder_roll_end"):
            # DISTANCE BETWEEN HUMERUS - RADIUS
            humerus_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_humerus_length")

            cmds.connectAttr(f"{self.prefix}_DEF_humerus.worldMatrix[0]", f"{humerus_length}.inMatrix1")
            cmds.connectAttr(f"{self.prefix}_DEF_radius.worldMatrix[0]", f"{humerus_length}.inMatrix2")

            # POSITION ROLL JOINTS
            cmds.setAttr(f"{arm_roll_scale_multiply}.input2.input2X", 0.5)
            cmds.connectAttr(f"{humerus_length}.distance", f"{arm_roll_scale_multiply}.input1.input1X")
            cmds.connectAttr(f"{arm_roll_scale_multiply}.output.outputX",
                             f"{self.prefix}_MCH_shoulder_roll_end.translate.translateY")

        if cmds.objExists(f"{self.prefix}_MCH_wrist_roll_end"):
            # DISTANCE BETWEEN RADIUS - WRIST
            radius_length = cmds.createNode("distanceBetween", name=f"{self.prefix}_radius_length")

            cmds.connectAttr(f"{self.prefix}_DEF_radius.worldMatrix[0]", f"{radius_length}.inMatrix1")
            cmds.connectAttr(f"{self.prefix}_DEF_wrist.worldMatrix[0]", f"{radius_length}.inMatrix2")

            # POSITION ROLL JOINTS
            cmds.setAttr(f"{arm_roll_scale_multiply}.input2.input2Y", 0.5)
            cmds.connectAttr(f"{radius_length}.distance", f"{arm_roll_scale_multiply}.input1.input1Y")
            cmds.connectAttr(f"{arm_roll_scale_multiply}.output.outputY",
                             f"{self.prefix}_MCH_wrist_roll_end.translate.translateY")

        # STRETCH ONLY IN IK AND DISABLE IT IN FK MODE
        # SCALE ROLL JOINTS
        arm_stretch_ik_blend = cmds.createNode("blendColors", name=f"{self.prefix}_arm_stretch_ik_blend")
        cmds.setAttr(f"{arm_stretch_ik_blend}.color1R", 1)
        cmds.setAttr(f"{arm_stretch_ik_blend}.color1G", 1)
        cmds.setAttr(f"{arm_stretch_ik_blend}.color1B", 1)
        cmds.setAttr(f"{arm_stretch_ik_blend}.color2R", 1)
        cmds.setAttr(f"{arm_stretch_ik_blend}.color2G", 1)
        cmds.setAttr(f"{arm_stretch_ik_blend}.color2B", 1)

        cmds.connectAttr(f"{self.prefix}_SWITCH_CTRL_arm.IK_FK_SWITCH", f"{arm_stretch_ik_blend}.blender")
        cmds.connectAttr(f"{arm_stretch_condition}.outColor.outColorR", f"{arm_stretch_ik_blend}.color1.color1R")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_shoulder_roll_end.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputR", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleY")

        # BLEND BETWEEN STRETCH AND NON STRETCH
        arm_stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_arm_stretch_blend")
        cmds.setAttr(f"{arm_stretch_blend}.color1R", 1)
        cmds.setAttr(f"{arm_stretch_blend}.color1G", 1)
        cmds.setAttr(f"{arm_stretch_blend}.color1B", 1)
        cmds.setAttr(f"{arm_stretch_blend}.color2R", 1)
        cmds.setAttr(f"{arm_stretch_blend}.color2G", 1)
        cmds.setAttr(f"{arm_stretch_blend}.color2B", 1)

        cmds.connectAttr(f"{self.prefix}_IK_CTRL_arm.Stretchiness", f"{arm_stretch_blend}.blender")
        # SCALE IK ARM JOINTS
        cmds.connectAttr(f"{arm_stretch_condition}.outColor.outColorR", f"{arm_stretch_blend}.color1.color1R")
        cmds.connectAttr(f"{arm_stretch_blend}.output.outputR", f"{self.prefix}_IK_humerus.scale.scaleY")
        cmds.connectAttr(f"{arm_stretch_blend}.output.outputR", f"{self.prefix}_IK_radius.scale.scaleY")

        # Preserve volume of mesh on stretch
        arm_volume_preservation = cmds.createNode("multiplyDivide", name=f"{self.prefix}_arm_volume_preservation")
        cmds.setAttr(f"{arm_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.setAttr(f"{arm_volume_preservation}.input2.input2X", -1)
        cmds.connectAttr(f"{arm_stretch_condition}.outColor.outColorR", f"{arm_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{arm_volume_preservation}.output.outputX", f"{arm_stretch_ik_blend}.color1.color1G")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_humerus.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_humerus.scale.scaleZ")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_radius.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_DEF_radius.scale.scaleZ")

        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_shoulder_roll_end.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_shoulder_roll_end.scale.scaleZ")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleX")
        cmds.connectAttr(f"{arm_stretch_ik_blend}.output.outputG", f"{self.prefix}_MCH_wrist_roll_end.scale.scaleZ")

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
