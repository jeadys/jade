import maya.cmds as cmds
import mechanisms.arm_stretch as arm_stretch_module
from joints.arm_bind import bake_transform_to_offset_parent_matrix
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape
from utilities.enums import RotateOrder
from dataclasses import dataclass

reload(control_shape)
reload(arm_stretch_module)


@dataclass(frozen=True)
class LegSegment:
    name: str
    shape: str


class IKLeg:
    def __init__(self, prefix) -> None:
        self.prefix = prefix
        self.leg_segments = (
            LegSegment(name="upperleg", shape="circle"),
            LegSegment(name="lowerleg", shape="circle"),
            LegSegment(name="ankle", shape="star"),
        )

        self.kinematic_parent_group = f"{self.prefix}_leg_kinematics"
        self.control_parent_group = f"{self.prefix}_leg_controls"
        self.control_shape: ControlShape = ControlShape()

    def create_ik_leg_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_ik_joint = self.kinematic_parent_group
        for count, joint in enumerate(self.leg_segments):
            current_ik_joint = cmds.duplicate(f"{self.prefix}_DEF_{joint.name}", parentOnly=True, name=f"{self.prefix}_IK_{joint.name}")[0]
            cmds.parentConstraint(f"{self.prefix}_IK_{joint.name}", f"{self.prefix}_DEF_{joint.name}", maintainOffset=True)
            cmds.parent(current_ik_joint, previous_ik_joint)

            bake_transform_to_offset_parent_matrix(current_ik_joint)

            previous_ik_joint = current_ik_joint

    def create_ik_leg_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        ik_leg_ctrl = self.control_shape.select_control_shape(shape="circle", name=f"{self.prefix}_IK_CTRL_leg")
        cmds.setAttr(f"{ik_leg_ctrl}.rotateOrder", RotateOrder.ZXY.value)

        ik_knee_ctrl = self.control_shape.select_control_shape(shape="star", name=f"{self.prefix}_IK_CTRL_knee")
        cmds.setAttr(f"{ik_knee_ctrl}.rotateOrder", RotateOrder.ZXY.value)

        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_leg",
            startJoint=f"{self.prefix}_IK_upperleg",
            endEffector=f"{self.prefix}_IK_ankle",
            solver="ikRPsolver")[0]

        # ANKLE
        cmds.matchTransform(ik_leg_ctrl, f"{self.prefix}_IK_ankle", position=True, rotation=True,scale=False)
        cmds.parent(ik_handle, ik_leg_ctrl)
        cmds.orientConstraint(ik_leg_ctrl, f"{self.prefix}_IK_ankle", maintainOffset=True)
        cmds.parent(ik_leg_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_leg_ctrl)

        # POLE
        cmds.matchTransform(ik_knee_ctrl, f"{self.prefix}_IK_lowerleg", position=True, rotation=False, scale=False)
        cmds.rotate(90, 0, 0, ik_knee_ctrl, relative=True)
        position = cmds.xform(ik_knee_ctrl, query=True, translation=True, worldSpace=True)
        cmds.move(position[0], position[1], position[2] + 75, ik_knee_ctrl)
        cmds.poleVectorConstraint(ik_knee_ctrl, ik_handle)
        cmds.parent(ik_knee_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_knee_ctrl)

    def create_knee_space_swap(self):
        cmds.addAttr(
            f"{self.prefix}_IK_CTRL_knee", attributeType="enum", enumName=f"WORLD=0:FOOT=1", niceName="KNEE_FOLLOW",
            longName="KNEE_FOLLOW", defaultValue=0, keyable=True
        )

        knee_space_swap = cmds.createNode("blendMatrix", name=f"{self.prefix}_blend_matrix_knee_space_swap")
        offset_matrix = cmds.getAttr(f"{self.prefix}_IK_CTRL_knee.offsetParentMatrix")
        cmds.setAttr(f"{knee_space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_leg_swap_position = cmds.spaceLocator(name=f"{self.prefix}_ik_leg_swap_position")
        cmds.matchTransform(ik_leg_swap_position, f"{self.prefix}_IK_CTRL_knee", position=True, rotation=True, scale=False)
        cmds.parent(ik_leg_swap_position, f"{self.prefix}_IK_CTRL_leg")

        bake_transform_to_offset_parent_matrix(ik_leg_swap_position[0])

        cmds.connectAttr(f"{ik_leg_swap_position[0]}.worldMatrix[0]", f"{knee_space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{knee_space_swap}.outputMatrix", f"{self.prefix}_IK_CTRL_knee.offsetParentMatrix")
        cmds.connectAttr(f"{self.prefix}_IK_CTRL_knee.KNEE_FOLLOW", f"{knee_space_swap}.envelope")

        cmds.addAttr(f"{self.prefix}_IK_CTRL_leg", longName="KNEE_FOLLOW", proxy=f"{self.prefix}_IK_CTRL_knee.KNEE_FOLLOW")