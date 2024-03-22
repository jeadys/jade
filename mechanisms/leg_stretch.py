import maya.cmds as cmds

from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.enums import Stretch, MUDOperation


class LegStretch:
    def __init__(self, prefix):
        self.prefix = prefix
        self.leg_segments = [f"{self.prefix}_upperleg", f"{self.prefix}_lowerleg", f"{self.prefix}_ankle"]
        self.kinematic_parent_group = f"{self.prefix}_leg_kinematics"

    def create_leg_stretch(self):
        self.create_leg_stretch_joints()
        self.create_leg_stretch_attributes()
        self.create_leg_stretch_nodes()

    def create_leg_stretch_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_stretch_joint = self.kinematic_parent_group
        for index, joint in enumerate(self.leg_segments):
            current_stretch_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_STRETCH")[0]
            cmds.parent(current_stretch_joint, previous_stretch_joint)
            cmds.setAttr(f"{current_stretch_joint}.visibility", False)

            bake_transform_to_offset_parent_matrix(current_stretch_joint)

            previous_stretch_joint = current_stretch_joint

    def create_leg_stretch_nodes(self):
        leg_stretch_length = cmds.createNode("plusMinusAverage", name=f"{self.prefix}_leg_stretch_length")
        leg_stretch_end_loc = cmds.spaceLocator(name=f"{self.prefix}_leg_stretch_end_LOC")[0]
        cmds.matchTransform(leg_stretch_end_loc, f"{self.prefix}_leg_IK_CTRL", position=True, rotation=True, scale=False)
        cmds.parent(leg_stretch_end_loc, f"{self.prefix}_leg_IK_CTRL")

        # JOINT TO JOINT DISTANCE OF leg
        for index, joint in enumerate(self.leg_segments[:-1]):
            distance_between_joints = cmds.createNode("distanceBetween", name=f"{joint}_distance_node")

            cmds.connectAttr(f"{joint}_STRETCH.worldMatrix", f"{distance_between_joints}.inMatrix1")
            cmds.connectAttr(f"{self.leg_segments[index + 1]}_STRETCH.worldMatrix",
                             f"{distance_between_joints}.inMatrix2")

            cmds.connectAttr(f"{joint}_STRETCH.rotatePivotTranslate", f"{distance_between_joints}.point1")
            cmds.connectAttr(f"{self.leg_segments[index + 1]}_STRETCH.rotatePivotTranslate",
                             f"{distance_between_joints}.point2")

            cmds.connectAttr(f"{joint}_distance_node.distance", f"{leg_stretch_length}.input1D[{index}]")

        # ROOT JOINT TO LOCATOR DISTANCE
        distance_between = cmds.createNode("distanceBetween", name=f"{self.prefix}_leg_distance_node")

        cmds.connectAttr(f"{self.leg_segments[0]}_STRETCH.worldMatrix", f"{distance_between}.inMatrix1")
        cmds.connectAttr(f"{leg_stretch_end_loc}.worldMatrix", f"{distance_between}.inMatrix2")

        cmds.connectAttr(f"{self.leg_segments[0]}_STRETCH.rotatePivotTranslate", f"{distance_between}.point1")
        cmds.connectAttr(f"{leg_stretch_end_loc}.rotatePivotTranslate", f"{distance_between}.point2")

        # leg SCALE FACTOR
        leg_scale_factor = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_scale_factor")
        cmds.setAttr(f"{leg_scale_factor}.operation", MUDOperation.DIVIDE.value)
        cmds.connectAttr(f"{distance_between}.distance", f"{leg_scale_factor}.input1X")
        cmds.connectAttr(f"{leg_stretch_length}.output1D", f"{leg_scale_factor}.input2X")

        # leg STRETCH CONDITION
        leg_stretch_condition = cmds.createNode("condition", name=f"{self.prefix}_leg_stretch_condition")
        cmds.setAttr(f"{leg_stretch_condition}.secondTerm", 1)
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Stretch_Type", f"{leg_stretch_condition}.operation")
        cmds.connectAttr(f"{leg_scale_factor}.outputX", f"{leg_stretch_condition}.firstTerm")

        # BLEND COLOR NODES
        color_attributes = ["R", "G", "B"]
        leg_stretch_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_blend")
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Stretchiness", f"{leg_stretch_blend}.blender")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{leg_stretch_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{leg_stretch_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{leg_scale_factor}.outputX", f"{leg_stretch_blend}.color1R")
        cmds.connectAttr(f"{leg_stretch_blend}.outputR", f"{leg_stretch_condition}.colorIfTrueR")

        leg_stretch_ik_blend = cmds.createNode("blendColors", name=f"{self.prefix}_leg_stretch_ik_blend")

        for color_attribute in color_attributes:
            cmds.setAttr(f"{leg_stretch_ik_blend}.color1{color_attribute}", 1)
            cmds.setAttr(f"{leg_stretch_ik_blend}.color2{color_attribute}", 1)

        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.IK_FK_SWITCH", f"{leg_stretch_ik_blend}.blender")
        cmds.connectAttr(f"{leg_stretch_condition}.outColorR", f"{leg_stretch_ik_blend}.color1R")

        # POSITION JOINTS ON STRETCH
        cmds.connectAttr(f"{leg_stretch_condition}.outColorR", f"{self.leg_segments[0]}_IK.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_condition}.outColorR", f"{self.leg_segments[1]}_IK.scale.scaleY")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputR", f"{self.leg_segments[1]}.scale.scaleY")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputR", f"{self.leg_segments[-1]}.scale.scaleY")

        twist_joints = ["a01", "b01", "c01", "d01", "a02", "b02", "c02", "d02"]
        for twist_joint in twist_joints:
            if cmds.objExists(f"{self.prefix}_leg_twist_{twist_joint}") and cmds.objExists(f"{self.prefix}_leg_twist_{twist_joint}"):
                cmds.connectAttr(f"{leg_stretch_ik_blend}.outputR", f"{self.prefix}_leg_twist_{twist_joint}.scaleY")

        # PRESERVE JOINTS VOLUME ON STRETCH
        leg_volume_preservation = cmds.createNode("multiplyDivide", name=f"{self.prefix}_leg_volume_preservation")
        cmds.setAttr(f"{leg_volume_preservation}.operation", MUDOperation.POWER.value)
        cmds.connectAttr(f"{self.prefix}_leg_IK_CTRL.Volume", f"{leg_volume_preservation}.input2X")
        cmds.connectAttr(f"{leg_stretch_blend}.outputR", f"{leg_volume_preservation}.input1.input1X")
        cmds.connectAttr(f"{leg_volume_preservation}.outputX", f"{leg_stretch_condition}.colorIfTrueG")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.leg_segments[1]}.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.leg_segments[1]}.scale.scaleZ")

        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.leg_segments[-1]}.scale.scaleX")
        cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.leg_segments[-1]}.scale.scaleZ")

        for twist_joint in twist_joints:
            if cmds.objExists(f"{self.prefix}_leg_twist_{twist_joint}"):
                cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.prefix}_leg_twist_{twist_joint}.scaleX")
                cmds.connectAttr(f"{leg_stretch_ik_blend}.outputG", f"{self.prefix}_leg_twist_{twist_joint}.scaleZ")

    def create_leg_stretch_attributes(self):
        # STRETCHINESS
        if not cmds.attributeQuery("Stretchiness", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(
                f"{self.prefix}_leg_IK_CTRL",
                attributeType="float",
                niceName="Stretchiness",
                longName="Stretchiness",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )

        if not cmds.attributeQuery("Volume", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(
                f"{self.prefix}_leg_IK_CTRL",
                attributeType="float",
                niceName="Volume",
                longName="Volume",
                defaultValue=-0.5,
                keyable=True,
            )

        # STRETCH TYPE
        if not cmds.attributeQuery("Stretch_Type", node=f"{self.prefix}_leg_IK_CTRL", exists=True):
            cmds.addAttr(f"{self.prefix}_leg_IK_CTRL",
                         attributeType="enum",
                         niceName="Stretch_Type",
                         longName="Stretch_Type",
                         defaultValue=Stretch.STRETCH.value,
                         enumName=f"{Stretch.BOTH.name}={Stretch.BOTH.value}:{Stretch.STRETCH.name}={Stretch.STRETCH.value}:{Stretch.SQUASH.name}={Stretch.SQUASH.value}",
                         keyable=True,
                         )
