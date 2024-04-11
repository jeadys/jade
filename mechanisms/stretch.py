import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import StretchMode, MUDOperation


class Stretch:
    def __init__(self, prefix: str, name: str, segments: list[str]):
        self.prefix = prefix
        self.name = name
        self.segments = segments
        self.kinematic_parent_group = f"{self.prefix}_{self.name}_kinematics"

    def create_stretch(self) -> None:
        self.create_stretch_joints()
        self.create_stretch_attributes()
        self.create_stretch_nodes()

    def create_stretch_joints(self) -> None:
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_stretch_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.segments):
            current_stretch_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_STRETCH")[0]
            cmds.parent(current_stretch_joint, previous_stretch_joint)
            cmds.setAttr(f"{current_stretch_joint}.visibility", False)

            bake_transform_to_offset_parent_matrix(current_stretch_joint)

            previous_stretch_joint = current_stretch_joint

    def create_stretch_nodes(self) -> None:
        stretch_length: str = cmds.createNode("plusMinusAverage", name=f"{self.prefix}_{self.name}_stretch_length")
        stretch_end_loc: str = cmds.spaceLocator(name=f"{self.prefix}_{self.name}_stretch_end_LOC")[0]
        cmds.matchTransform(stretch_end_loc, f"{self.prefix}_{self.name}_IK_CTRL", position=True, rotation=True,
                            scale=False)
        cmds.parent(stretch_end_loc, f"{self.prefix}_{self.name}_IK_CTRL")

        # JOINT TO JOINT DISTANCE OF SEGMENT
        for index, joint in enumerate(self.segments[:-1]):
            distance_between_joints = cmds.createNode("distanceBetween", name=f"{joint}_distance_node")

            cmds.connectAttr(f"{joint}_STRETCH.worldMatrix", f"{distance_between_joints}.inMatrix1")
            cmds.connectAttr(f"{self.segments[index + 1]}_STRETCH.worldMatrix",
                             f"{distance_between_joints}.inMatrix2")

            cmds.connectAttr(f"{joint}_STRETCH.rotatePivotTranslate", f"{distance_between_joints}.point1")
            cmds.connectAttr(f"{self.segments[index + 1]}_STRETCH.rotatePivotTranslate",
                             f"{distance_between_joints}.point2")

            cmds.connectAttr(f"{joint}_distance_node.distance", f"{stretch_length}.input1D[{index}]")

        # ROOT JOINT TO LOCATOR DISTANCE
        distance_between: str = cmds.createNode("distanceBetween", name=f"{self.prefix}_{self.name}_distance_node")

        cmds.connectAttr(f"{self.segments[0]}_STRETCH.worldMatrix", f"{distance_between}.inMatrix1")
        cmds.connectAttr(f"{stretch_end_loc}.worldMatrix", f"{distance_between}.inMatrix2")

        cmds.connectAttr(f"{self.segments[0]}_STRETCH.rotatePivotTranslate", f"{distance_between}.point1")
        cmds.connectAttr(f"{stretch_end_loc}.rotatePivotTranslate", f"{distance_between}.point2")

        # SEGMENT SCALE FACTOR
        scale_factor: str = cmds.createNode("multiplyDivide", name=f"{self.prefix}_{self.name}_scale_factor")
        cmds.setAttr(f"{scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{distance_between}.distance", f"{scale_factor}.input1X")
        cmds.connectAttr(f"{stretch_length}.output1D", f"{scale_factor}.input2X")

        # SEGMENT STRETCH CONDITION
        stretch_condition: str = cmds.createNode("condition", name=f"{self.prefix}_{self.name}_stretch_condition")
        cmds.setAttr(f"{stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{self.prefix}_{self.name}_IK_CTRL.Stretch_Type", f"{stretch_condition}.operation")
        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_condition}.firstTerm")

        # BLEND COLOR NODES
        color_attributes: list[str] = ["R", "G", "B"]
        stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_{self.name}_stretch_blend")
        cmds.connectAttr(f"{self.prefix}_{self.name}_IK_CTRL.Stretchiness", f"{stretch_blend}.blender")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_blend}.color1R")
        cmds.connectAttr(f"{stretch_blend}.outputR", f"{stretch_condition}.colorIfTrueR")

        stretch_ik_blend: str = cmds.createNode("blendColors", name=f"{self.prefix}_{self.name}_stretch_ik_blend")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_ik_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_{self.name}_IK_CTRL.{self.prefix}_{self.name}_IK_FK_SWITCH",
                         f"{stretch_ik_blend}.blender")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{stretch_ik_blend}.color1R")

        # POSITION JOINTS ON STRETCH
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{self.segments[0]}_IK.scale.scaleY")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{self.segments[1]}_IK.scale.scaleY")

        cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{self.segments[1]}.scale.scaleY")
        # cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{self.segments[-1]}.scale.scaleY")

        twist_joints: list[str] = ["a01", "b01", "c01", "d01", "a02", "b02", "c02", "d02"]
        for twist_joint in twist_joints:
            if cmds.objExists(f"{self.prefix}_{self.name}_twist_{twist_joint}") and cmds.objExists(
                    f"{self.prefix}_{self.name}_twist_{twist_joint}"):
                cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{self.prefix}_{self.name}_twist_{twist_joint}.scaleY")

        # PRESERVE JOINTS VOLUME ON STRETCH
        volume_preservation: str = cmds.createNode("multiplyDivide",
                                                   name=f"{self.prefix}_{self.name}_volume_preservation")
        cmds.setAttr(f"{volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.connectAttr(f"{self.prefix}_{self.name}_IK_CTRL.Volume", f"{volume_preservation}.input2X")
        cmds.connectAttr(f"{stretch_blend}.outputR", f"{volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{volume_preservation}.outputX", f"{stretch_condition}.colorIfTrueG")

        cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.segments[1]}.scale.scaleX")
        cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.segments[1]}.scale.scaleZ")

        # cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.segments[-1]}.scale.scaleX")
        # cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.segments[-1]}.scale.scaleZ")

        for twist_joint in twist_joints:
            if cmds.objExists(f"{self.prefix}_{self.name}_twist_{twist_joint}"):
                cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.prefix}_{self.name}_twist_{twist_joint}.scaleX")
                cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{self.prefix}_{self.name}_twist_{twist_joint}.scaleZ")

    def create_stretch_attributes(self) -> None:
        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node=f"{self.prefix}_{self.name}_IK_CTRL", exists=True):
            cmds.addAttr(
                f"{self.prefix}_{self.name}_IK_CTRL",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Volume", node=f"{self.prefix}_{self.name}_IK_CTRL", exists=True):
            cmds.addAttr(
                f"{self.prefix}_{self.name}_IK_CTRL",
                attributeType="float",
                niceName="Volume",
                longName="Volume",
                defaultValue=-0.5,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node=f"{self.prefix}_{self.name}_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_{self.name}_IK_CTRL",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=StretchMode.STRETCH.value,
                         enumName=f"{StretchMode.BOTH.name}={StretchMode.BOTH.value}:{StretchMode.STRETCH.name}={StretchMode.STRETCH.value}:{StretchMode.SQUASH.name}={StretchMode.SQUASH.value}",
                         keyable=True,
                         )
