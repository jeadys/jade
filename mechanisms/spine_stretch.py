import maya.cmds as cmds

from utilities.enums import MUDOperation
from enum import Enum


class Stretch(Enum):
    BOTH = 1
    STRETCH = 3
    SQUASH = 5


class SpineStretch:

    def __init__(self):
        pass

    def create_spine_stretch_locators(self):
        pass

    def create_spine_stretch_joints(self):
        pass

    @staticmethod
    def create_spine_stretch_nodes():
        # Get length if spine curve
        spine_curve_info = cmds.createNode("curveInfo", name="spine_curve_info")
        curve_shape = cmds.listRelatives("curve_spine", shapes=True)[0]

        cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{spine_curve_info}.inputCurve")

        spine_scale_factor = cmds.createNode("multiplyDivide", name="spine_scale_factor")
        cmds.setAttr(f"{spine_scale_factor}.operation", MUDOperation.DIVIDE.value)

        cmds.connectAttr(f"{spine_curve_info}.arcLength", f"{spine_scale_factor}.input1.input1X")
        copied_value = cmds.getAttr(f"{spine_scale_factor}.input1.input1X")
        cmds.setAttr(f"{spine_scale_factor}.input2.input2X", copied_value)

        spine_stretch_blend = cmds.createNode("blendColors", name="spine_stretch_blend")
        cmds.setAttr(f"{spine_stretch_blend}.color1R", 1)
        cmds.setAttr(f"{spine_stretch_blend}.color1G", 1)
        cmds.setAttr(f"{spine_stretch_blend}.color1B", 1)
        cmds.setAttr(f"{spine_stretch_blend}.color2R", 1)
        cmds.setAttr(f"{spine_stretch_blend}.color2G", 1)
        cmds.setAttr(f"{spine_stretch_blend}.color2B", 1)

        cmds.connectAttr(f"{spine_scale_factor}.output.outputX", f"{spine_stretch_blend}.color1.color1R")

        spine_stretch_ik_blend = cmds.createNode("blendColors", name="spine_stretch_ik_blend")
        cmds.setAttr(f"{spine_stretch_ik_blend}.color1R", 1)
        cmds.setAttr(f"{spine_stretch_ik_blend}.color1G", 1)
        cmds.setAttr(f"{spine_stretch_ik_blend}.color1B", 1)
        cmds.setAttr(f"{spine_stretch_ik_blend}.color2R", 1)
        cmds.setAttr(f"{spine_stretch_ik_blend}.color2G", 1)
        cmds.setAttr(f"{spine_stretch_ik_blend}.color2B", 1)

        cmds.connectAttr("IK_CTRL_cog.Stretchiness", f"{spine_stretch_blend}.blender")

        # Check if spine should stretch or not
        spine_stretch_condition = cmds.createNode("condition", name="spine_stretch_condition")
        cmds.setAttr(f"{spine_stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{spine_scale_factor}.output.outputX", f"{spine_stretch_condition}.firstTerm")
        cmds.connectAttr(f"{spine_stretch_blend}.output.outputR", f"{spine_stretch_condition}.colorIfTrue.colorIfTrueR")

        # Determines if spine should SQUASH, STRETCH or BOTH
        cmds.connectAttr("IK_CTRL_cog.Stretch_Type", f"{spine_stretch_condition}.operation")

        cmds.connectAttr(f"{spine_stretch_condition}.outColor.outColorR", f"{spine_stretch_ik_blend}.color1.color1R")
        cmds.connectAttr(f"IK_CTRL_cog.IK_FK_SWITCH", f"{spine_stretch_ik_blend}.blender")

        # Scale the IK spines correctly
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "IK_spine_01.scale.scaleY")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "IK_spine_02.scale.scaleY")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "IK_spine_03.scale.scaleY")

        # Scale the DEF spines correctly
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "DEF_spine_01.scale.scaleY")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "DEF_spine_02.scale.scaleY")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputR", "DEF_spine_03.scale.scaleY")

        # Preserve volume of mesh on stretch
        spine_volume_preservation = cmds.createNode("multiplyDivide", name="spine_volume_preservation")
        cmds.setAttr(f"{spine_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.setAttr(f"{spine_volume_preservation}.input2.input2X", -1)
        cmds.connectAttr(f"{spine_stretch_condition}.outColor.outColorR", f"{spine_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{spine_volume_preservation}.output.outputX", f"{spine_stretch_ik_blend}.color1.color1G")

        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_01.scale.scaleX")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_01.scale.scaleZ")

        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_02.scale.scaleX")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_02.scale.scaleZ")

        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_03.scale.scaleX")
        cmds.connectAttr(f"{spine_stretch_ik_blend}.output.outputG", "DEF_spine_03.scale.scaleZ")

    @staticmethod
    def create_spine_stretch_attributes():
        # CATEGORY STRETCH
        if not cmds.attributeQuery("STRETCH", node="IK_CTRL_cog", exists=True):
            cmds.addAttr("IK_CTRL_cog", attributeType="enum", niceName="STRETCH", longName="STRETCH",
                         enumName="---------")
            cmds.setAttr("IK_CTRL_cog.STRETCH", keyable=False, lock=True, channelBox=True)

        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node="IK_CTRL_cog", exists=True):
            cmds.addAttr(
                "IK_CTRL_cog",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node="IK_CTRL_cog", exists=True):
            cmds.addAttr("IK_CTRL_cog",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=Stretch.STRETCH.value,
                         enumName=f"{Stretch.BOTH.name}={Stretch.BOTH.value}:{Stretch.STRETCH.name}={Stretch.STRETCH.value}:{Stretch.SQUASH.name}={Stretch.SQUASH.value}",
                         keyable=True,
                         )
