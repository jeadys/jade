import maya.cmds as cmds
from enum import Enum


class WorldUpType(Enum):
    SCENE_UP = 0
    OBJECT_UP = 1
    OBJECT_UP_START_END = 2
    OBJECT_ROTATION_UP = 3
    OBJECT_ROTATION_UP_START_END = 4
    VECTOR = 5
    VECTOR_START_END = 6
    RELATIVE = 7


class ForwardAxis(Enum):
    POSITIVE_X = 0
    NEGATIVE_X = 1
    POSITIVE_Y = 2
    NEGATIVE_Y = 3
    POSITIVE_Z = 4
    NEGATIVE_Z = 5


class UpAxis(Enum):
    POSITIVE_Y = 0
    NEGATIVE_Y = 1
    CLOSEST_Y = 2
    POSITIVE_Z = 3
    NEGATIVE_Z = 4
    CLOSEST_Z = 5
    POSITIVE_X = 6
    NEGATIVE_X = 7
    CLOSEST_X = 8


class SpineRoll:

    def __init__(self):
        pass

    def create_spine_roll_locators(self):
        pass

    def create_spine_roll_joints(self):
        pass

    @staticmethod
    def create_spine_roll_nodes():
        twist_offset_multiply = cmds.createNode("multiplyDivide", name="twist_offset_multiply")
        cmds.setAttr(f"{twist_offset_multiply}.input2.input2X", -1)

        cmds.connectAttr("IK_CTRL_hip.rotate.rotateY", f"{twist_offset_multiply}.input1.input1X")

        shoulder_twist_pma = cmds.createNode("plusMinusAverage", name="shoulder_twist_plus_minus_average")
        cmds.connectAttr(f"{twist_offset_multiply}.output.outputX", f"{shoulder_twist_pma}.input1D[0]")
        cmds.connectAttr("IK_CTRL_shoulder.rotate.rotateY", f"{shoulder_twist_pma}.input1D[1]")
        cmds.connectAttr(f"{shoulder_twist_pma}.output1D", "ikHandle_spine.twist")
        cmds.connectAttr("IK_CTRL_chest.rotate.rotateY", f"{shoulder_twist_pma}.input1D[2]")
        # cmds.connectAttr("CTRL_root.rotate.rotateY", f"{shoulder_twist_pma}.input1D[3]")

        hip_twist_pma = cmds.createNode("plusMinusAverage", name="hip_twist_plus_minus_average")
        cmds.connectAttr("IK_CTRL_hip.rotate.rotateY", f"{hip_twist_pma}.input1D[0]")
        cmds.connectAttr("IK_CTRL_pelvis.rotate.rotateY", f"{hip_twist_pma}.input1D[1]")
        cmds.connectAttr(f"{hip_twist_pma}.output1D", "ikHandle_spine.roll")

    @staticmethod
    def create_spine_roll_attributes():
        cmds.setAttr("ikHandle_spine.dTwistControlEnable", True)
        cmds.setAttr("ikHandle_spine.dWorldUpType", WorldUpType.OBJECT_ROTATION_UP_START_END.value)
        cmds.setAttr("ikHandle_spine.dForwardAxis", ForwardAxis.POSITIVE_Y.value)
        cmds.setAttr("ikHandle_spine.dWorldUpAxis", UpAxis.POSITIVE_Z.value)

        cmds.setAttr("ikHandle_spine.dWorldUpVectorX", 0)
        cmds.setAttr("ikHandle_spine.dWorldUpVectorEndX", 0)
        cmds.setAttr("ikHandle_spine.dWorldUpVectorY", 0)
        cmds.setAttr("ikHandle_spine.dWorldUpVectorEndY", 0)
        cmds.setAttr("ikHandle_spine.dWorldUpVectorZ", 1)
        cmds.setAttr("ikHandle_spine.dWorldUpVectorEndZ", 1)

        # cmds.setAttr("ikHandle_spine.dWorldUpObject", "IK_CTRL_hip", type="string")
        # cmds.setAttr("ikHandle_spine.dWorldUpObjectEnd", "IK_CTRL_shoulder", type="string")
