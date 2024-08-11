import maya.cmds as cmds

from data.rig_structure import Segment
from utilities.relations import has_parent
from utilities.enums import MUDOperation, StretchMode


class Stretch:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.side = cmds.getAttr(f"{self.node}.side")
        self.module_nr = cmds.getAttr(f"{self.node}.module_nr")
        self.prefix = f"{self.side}{self.name}_{self.module_nr}"

    def stretch_joint(self, segments: list[Segment]) -> list[str]:
        joint_group = f"{self.prefix}_STRETCH_GROUP"
        if not cmds.objExists(joint_group):
            cmds.group(empty=True, name=joint_group)

        joint_layer_group = f"{self.prefix}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)

        if not has_parent(joint_group, joint_layer_group):
            cmds.parent(joint_group, joint_layer_group)

        stretch_joints = []
        for segment in segments:
            if cmds.objExists(f"{segment}_STRETCH"):
                continue

            current_segment = cmds.duplicate(f"{segment}_JNT", name=f"{segment}_STRETCH", parentOnly=True)[0]

            parent_joint = cmds.listRelatives(segment, parent=True, shapes=False, type="transform")
            if parent_joint and cmds.objExists(f"{parent_joint[0]}_STRETCH"):
                cmds.parent(current_segment, f"{parent_joint[0]}_STRETCH")
            else:
                cmds.parent(current_segment, joint_group)

            cmds.setAttr(f"{current_segment}.visibility", False)

            stretch_joints.append(current_segment)

        return stretch_joints

    def stretch_node(self, segments: list[Segment], main_control):
        stretch_length: str = cmds.createNode("plusMinusAverage", name=f"{self.prefix}_stretch_length")
        stretch_end_loc: str = cmds.spaceLocator(name=f"{self.prefix}_stretch_end_LOC")[0]
        cmds.matchTransform(stretch_end_loc, main_control, position=True, rotation=True, scale=False)
        cmds.parent(stretch_end_loc, main_control)

        # JOINT TO JOINT DISTANCE OF SEGMENT
        for index, segment in enumerate(segments[:-1]):
            distance_between_joints = cmds.createNode("distanceBetween",
                                                      name=f"{segment}_distance_node")

            cmds.connectAttr(f"{segment}_STRETCH.worldMatrix", f"{distance_between_joints}.inMatrix1")
            cmds.connectAttr(f"{segments[index + 1]}_STRETCH.worldMatrix", f"{distance_between_joints}.inMatrix2")

            cmds.connectAttr(f"{segment}_STRETCH.rotatePivotTranslate", f"{distance_between_joints}.point1")
            cmds.connectAttr(f"{segments[index + 1]}_STRETCH.rotatePivotTranslate", f"{distance_between_joints}.point2")

            cmds.connectAttr(f"{distance_between_joints}.distance", f"{stretch_length}.input1D[{index}]")

        # ROOT JOINT TO LOCATOR DISTANCE
        distance_between: str = cmds.createNode("distanceBetween", name=f"{self.prefix}_distance_node")

        cmds.connectAttr(f"{segments[0]}_STRETCH.worldMatrix", f"{distance_between}.inMatrix1")
        cmds.connectAttr(f"{stretch_end_loc}.worldMatrix", f"{distance_between}.inMatrix2")

        cmds.connectAttr(f"{segments[0]}_STRETCH.rotatePivotTranslate", f"{distance_between}.point1")
        cmds.connectAttr(f"{stretch_end_loc}.rotatePivotTranslate", f"{distance_between}.point2")

        # SEGMENT SCALE FACTOR
        scale_factor: str = cmds.createNode("multiplyDivide", name=f"{self.prefix}_scale_factor")
        cmds.setAttr(f"{scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{distance_between}.distance", f"{scale_factor}.input1X")
        cmds.connectAttr(f"{stretch_length}.output1D", f"{scale_factor}.input2X")

        # SEGMENT STRETCH CONDITION
        stretch_condition: str = cmds.createNode("condition", name=f"{self.prefix}_stretch_condition")
        cmds.setAttr(f"{stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{main_control}.Stretch_Type", f"{stretch_condition}.operation")
        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_condition}.firstTerm")

        # BLEND COLOR NODES
        color_attributes: list[str] = ["R", "G", "B"]
        stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_stretch_blend")
        cmds.connectAttr(f"{main_control}.Stretchiness", f"{stretch_blend}.blender")

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
        for segment in segments[:-1]:
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{segment}_JNT.scale.scaleX")
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{segment}_IK.scale.scaleX")

        # PRESERVE JOINTS VOLUME ON STRETCH
        volume_preservation: str = cmds.createNode("multiplyDivide", name=f"{self.prefix}_volume_preservation")
        cmds.setAttr(f"{volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.connectAttr(f"{main_control}.Volume", f"{volume_preservation}.input2X")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{volume_preservation}.input1X")
        cmds.connectAttr(f"{volume_preservation}.outputX", f"{stretch_ik_blend}.color1G")

        for segment in segments[-2:]:
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segment}_JNT.scale.scaleY")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segment}_JNT.scale.scaleZ")

        if cmds.objExists(f"{self.prefix}_TWIST_start_forward"):
            self.stretch_twist_joint(stretch_ik_blend=stretch_ik_blend,
                                     twist_start_joint=f"{self.prefix}_TWIST_start_forward")

        if cmds.objExists(f"{self.prefix}_TWIST_start_backward"):
            self.stretch_twist_joint(stretch_ik_blend=stretch_ik_blend,
                                     twist_start_joint=f"{self.prefix}_TWIST_start_backward")

    @staticmethod
    def stretch_twist_joint(stretch_ik_blend, twist_start_joint):
        twist_start_children = cmds.listRelatives(twist_start_joint, shapes=False, type="joint", allDescendents=True)
        for twist_joint in [twist_start_joint] + twist_start_children:
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{twist_joint}.scaleX")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{twist_joint}.scaleY")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{twist_joint}.scaleZ")

    def stretch_attribute(self, main_control):
        if not cmds.attributeQuery("Stretchiness", node=main_control, exists=True):
            cmds.addAttr(
                main_control,
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Volume", node=main_control, exists=True):
            cmds.addAttr(
                main_control,
                attributeType="float",
                niceName="Volume",
                longName="Volume",
                defaultValue=-0.5,
                minValue=-1,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Stretch_Type", node=main_control, exists=True):
            cmds.addAttr(
                main_control,
                attributeType="enum",
                niceName="Stretch_Type",
                longName="Stretch_Type",
                defaultValue=StretchMode.STRETCH.value,
                enumName=StretchMode.enum_to_string_attribute(),
                keyable=True,
            )
