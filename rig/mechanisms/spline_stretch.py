import maya.cmds as cmds

from utilities.enums import MUDOperation, StretchMode


class SplineStretch:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"

    def stretch_node(self, segments, curve, control):
        curve_info = cmds.createNode("curveInfo", name=f"{self.prefix}_curve_info")
        curve_shape = cmds.listRelatives(curve, shapes=True)[0]

        cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{curve_info}.inputCurve")

        # SEGMENT SCALE FACTOR
        scale_factor = cmds.createNode("multiplyDivide", name=f"{self.prefix}_scale_factor")
        cmds.setAttr(f"{scale_factor}.operation", MUDOperation.DIVIDE.value)

        cmds.connectAttr(f"{curve_info}.arcLength", f"{scale_factor}.input1X")
        copied_value = cmds.getAttr(f"{scale_factor}.input1X")
        cmds.setAttr(f"{scale_factor}.input2X", copied_value)

        # SEGMENT STRETCH CONDITION
        stretch_condition: str = cmds.createNode("condition", name=f"{self.prefix}_stretch_condition")
        cmds.setAttr(f"{stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{control}.Stretch_Type", f"{stretch_condition}.operation")
        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_condition}.firstTerm")

        # BLEND COLOR NODES
        color_attributes: list[str] = ["R", "G", "B"]
        stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_stretch_blend")
        cmds.connectAttr(f"{control}.Stretchiness", f"{stretch_blend}.blender")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_blend}.color1R")
        cmds.connectAttr(f"{stretch_blend}.outputR", f"{stretch_condition}.colorIfTrueR")

        stretch_ik_blend: str = cmds.createNode("blendColors", name=f"{self.prefix}_stretch_ik_blend")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_ik_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"switch_control.{self.prefix}_switch", f"{stretch_ik_blend}.blender")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{stretch_ik_blend}.color1R")

        # POSITION JOINTS ON STRETCH
        for segment in segments:
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{segment}_JNT.scale.scaleX")
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{segment}_IK.scale.scaleX")

        # PRESERVE JOINTS VOLUME ON STRETCH
        volume_preservation: str = cmds.createNode("multiplyDivide", name=f"{self.prefix}_volume_preservation")
        cmds.setAttr(f"{volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.connectAttr(f"{control}.Volume", f"{volume_preservation}.input2X")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{volume_preservation}.input1X")
        cmds.connectAttr(f"{volume_preservation}.outputX", f"{stretch_ik_blend}.color1G")

        for segment in segments:
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segment}_JNT.scale.scaleY")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segment}_JNT.scale.scaleZ")

    @staticmethod
    def stretch_attribute(control):
        if not cmds.attributeQuery("Stretchiness", node=control, exists=True):
            cmds.addAttr(
                control,
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Volume", node=control, exists=True):
            cmds.addAttr(
                control,
                attributeType="float",
                niceName="Volume",
                longName="Volume",
                defaultValue=-0.5,
                minValue=-1,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Stretch_Type", node=control, exists=True):
            cmds.addAttr(
                control,
                attributeType="enum",
                niceName="Stretch_Type",
                longName="Stretch_Type",
                defaultValue=StretchMode.STRETCH.value,
                enumName=StretchMode.enum_to_string_attribute(),
                keyable=True,
            )
