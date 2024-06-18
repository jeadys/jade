import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import StretchMode, MUDOperation
from modular.biped.biped import Segment


class Stretch:

    def __init__(self, node, name):
        self.node = node
        self.name = name
        self.blueprint_nr = self.node.rsplit("_", 1)[-1]
        self.selection = cmds.listConnections(f"{self.node}.parent_joint")

    def stretch_joint(self, prefix, segments: list[Segment]) -> list[str]:
        joint_group = cmds.group(empty=True, name=f"{prefix}{self.name}_{self.blueprint_nr}_STRETCH_GROUP")

        joint_layer_group = f"{prefix}{self.name}_{self.blueprint_nr}_LAYER_GROUP"
        if not cmds.objExists(joint_layer_group):
            joint_layer_group = cmds.group(empty=True, name=joint_layer_group)
        cmds.parent(joint_group, joint_layer_group)

        ik_joints = []
        for segment in segments:
            if cmds.objExists(f"{prefix}{segment.name}_{self.blueprint_nr}_STRETCH"):
                continue

            current_segment = cmds.duplicate(f"{prefix}{segment.name}_{self.blueprint_nr}_JNT",
                                             name=f"{prefix}{segment.name}_{self.blueprint_nr}_STRETCH",
                                             parentOnly=True)[0]

            if segment.control.parent is not None:
                cmds.parent(current_segment, f"{prefix}{segment.parent.name}_{self.blueprint_nr}_STRETCH")
            else:
                cmds.parent(current_segment, joint_group)

            cmds.setAttr(f"{current_segment}.visibility", False)

            ik_joints.append(current_segment)

        return ik_joints

    def stretch_node(self, prefix, segments: list[Segment]):
        stretch_length: str = cmds.createNode("plusMinusAverage",
                                              name=f"{prefix}{self.name}_{self.blueprint_nr}_stretch_length")
        stretch_end_loc: str = cmds.spaceLocator(name=f"{prefix}{self.name}_{self.blueprint_nr}_stretch_end_LOC")[0]
        cmds.matchTransform(stretch_end_loc, f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL", position=True,
                            rotation=True,
                            scale=False)
        cmds.parent(stretch_end_loc, f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL")

        # JOINT TO JOINT DISTANCE OF SEGMENT
        for index, segment in enumerate(segments[:-1]):
            distance_between_joints = cmds.createNode("distanceBetween",
                                                      name=f"{prefix}{segment.name}_{self.blueprint_nr}_distance_node")

            cmds.connectAttr(f"{prefix}{segment.name}_{self.blueprint_nr}_STRETCH.worldMatrix",
                             f"{distance_between_joints}.inMatrix1")
            cmds.connectAttr(f"{prefix}{segments[index + 1].name}_{self.blueprint_nr}_STRETCH.worldMatrix",
                             f"{distance_between_joints}.inMatrix2")

            cmds.connectAttr(f"{prefix}{segment.name}_{self.blueprint_nr}_STRETCH.rotatePivotTranslate",
                             f"{distance_between_joints}.point1")
            cmds.connectAttr(f"{prefix}{segments[index + 1].name}_{self.blueprint_nr}_STRETCH.rotatePivotTranslate",
                             f"{distance_between_joints}.point2")

            cmds.connectAttr(f"{distance_between_joints}.distance", f"{stretch_length}.input1D[{index}]")

        # ROOT JOINT TO LOCATOR DISTANCE
        distance_between: str = cmds.createNode("distanceBetween",
                                                name=f"{prefix}{self.name}_{self.blueprint_nr}_distance_node")

        cmds.connectAttr(f"{prefix}{segments[0].name}_{self.blueprint_nr}_STRETCH.worldMatrix",
                         f"{distance_between}.inMatrix1")
        cmds.connectAttr(f"{stretch_end_loc}.worldMatrix", f"{distance_between}.inMatrix2")

        cmds.connectAttr(f"{prefix}{segments[0].name}_{self.blueprint_nr}_STRETCH.rotatePivotTranslate",
                         f"{distance_between}.point1")
        cmds.connectAttr(f"{stretch_end_loc}.rotatePivotTranslate", f"{distance_between}.point2")

        # SEGMENT SCALE FACTOR
        scale_factor: str = cmds.createNode("multiplyDivide",
                                            name=f"{prefix}{self.name}_{self.blueprint_nr}_scale_factor")
        cmds.setAttr(f"{scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{distance_between}.distance", f"{scale_factor}.input1X")
        cmds.connectAttr(f"{stretch_length}.output1D", f"{scale_factor}.input2X")

        # SEGMENT STRETCH CONDITION
        stretch_condition: str = cmds.createNode("condition",
                                                 name=f"{prefix}{self.name}_{self.blueprint_nr}_stretch_condition")
        cmds.setAttr(f"{stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL.Stretch_Type",
                         f"{stretch_condition}.operation")
        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_condition}.firstTerm")

        # BLEND COLOR NODES
        color_attributes: list[str] = ["R", "G", "B"]
        stretch_blend = cmds.createNode("blendColors", name=f"{prefix}{self.name}_{self.blueprint_nr}_stretch_blend")
        cmds.connectAttr(f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL.Stretchiness", f"{stretch_blend}.blender")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{scale_factor}.outputX", f"{stretch_blend}.color1R")
        cmds.connectAttr(f"{stretch_blend}.outputR", f"{stretch_condition}.colorIfTrueR")

        stretch_ik_blend: str = cmds.createNode("blendColors",
                                                name=f"{prefix}{self.name}_{self.blueprint_nr}_stretch_ik_blend")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{stretch_ik_blend}.color2{color_attribute}", 1)

        # cmds.connectAttr(f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL.{prefix}{self.name}_IK_FK_SWITCH",
        #                  f"{stretch_ik_blend}.blender")

        cmds.connectAttr(f"switch_control.{prefix}{self.name}_{self.blueprint_nr}_switch",
                         f"{stretch_ik_blend}.blender")
        cmds.connectAttr(f"{stretch_condition}.outColorR", f"{stretch_ik_blend}.color1R")

        # POSITION JOINTS ON STRETCH
        cmds.connectAttr(f"{stretch_condition}.outColorR",
                         f"{prefix}{segments[0].name}_{self.blueprint_nr}_IK.scale.scaleY")
        cmds.connectAttr(f"{stretch_condition}.outColorR",
                         f"{prefix}{segments[1].name}_{self.blueprint_nr}_IK.scale.scaleY")

        cmds.connectAttr(f"{stretch_ik_blend}.outputR",
                         f"{prefix}{segments[1].name}_{self.blueprint_nr}_JNT.scale.scaleY")
        # cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{segments[-1]}.scale.scaleY")

        if cmds.objExists(f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_forward"):
            self.stretch_twist_joint(stretch_ik_blend=stretch_ik_blend,
                                     twist_start_joint=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_forward")

        if cmds.objExists(f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_backward"):
            self.stretch_twist_joint(stretch_ik_blend=stretch_ik_blend,
                                     twist_start_joint=f"{prefix}{self.name}_{self.blueprint_nr}_TWIST_start_backward")

        # PRESERVE JOINTS VOLUME ON STRETCH
        volume_preservation: str = cmds.createNode("multiplyDivide",
                                                   name=f"{prefix}{self.name}_{self.blueprint_nr}_volume_preservation")
        cmds.setAttr(f"{volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.connectAttr(f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL.Volume", f"{volume_preservation}.input2X")
        cmds.connectAttr(f"{stretch_blend}.outputR", f"{volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{volume_preservation}.outputX", f"{stretch_condition}.colorIfTrueG")

        cmds.connectAttr(f"{stretch_ik_blend}.outputG",
                         f"{prefix}{segments[1].name}_{self.blueprint_nr}_JNT.scale.scaleX")
        cmds.connectAttr(f"{stretch_ik_blend}.outputG",
                         f"{prefix}{segments[1].name}_{self.blueprint_nr}_JNT.scale.scaleZ")

        # cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segments[-1]}.scale.scaleX")
        # cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{segments[-1]}.scale.scaleZ")

    @staticmethod
    def stretch_twist_joint(stretch_ik_blend, twist_start_joint):
        twist_start_children = cmds.listRelatives(twist_start_joint, shapes=False, type="joint", allDescendents=True)
        for twist_joint in [twist_start_joint] + twist_start_children:
            cmds.connectAttr(f"{stretch_ik_blend}.outputR", f"{twist_joint}.scaleY")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{twist_joint}.scaleX")
            cmds.connectAttr(f"{stretch_ik_blend}.outputG", f"{twist_joint}.scaleZ")

    def stretch_attribute(self, prefix):
        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL",
                                   exists=True):
            cmds.addAttr(
                f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Volume", node=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL", exists=True):
            cmds.addAttr(
                f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL",
                attributeType="float",
                niceName="Volume",
                longName="Volume",
                defaultValue=-0.5,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node=f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL",
                                   exists=True):
            cmds.addAttr(f"{prefix}{self.name}_{self.blueprint_nr}_IK_CTRL",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=StretchMode.STRETCH.value,
                         enumName=f"{StretchMode.BOTH.name}={StretchMode.BOTH.value}:{StretchMode.STRETCH.name}={StretchMode.STRETCH.value}:{StretchMode.SQUASH.name}={StretchMode.SQUASH.value}",
                         keyable=True,
                         )

    # def generate_stretch_arm(self):
    #     self.stretch_joint()
    #     self.stretch_node()
    #     self.stretch_attribute()
