import maya.cmds as cmds
from utilities.bake_transform import bake_transform_to_offset_parent_matrix
from utilities.curve import Curve
from importlib import reload
import utilities.curve as control_shape
from utilities.enums import RotateOrder

reload(control_shape)


# @dataclass(frozen=True)
# class legSegment:
#     name: str
#     shape: str
#

class LegIK:
    def __init__(self, prefix, rotation_order) -> None:
        self.prefix = prefix
        self.rotation_order = rotation_order.upper()
        self.leg_segments = [f"{self.prefix}_upperleg", f"{self.prefix}_lowerleg", f"{self.prefix}_ankle",
                             f"{self.prefix}_ball", f"{self.prefix}_toe"]
        self.kinematic_parent_group = f"{self.prefix}_leg_kinematics"
        self.control_parent_group = f"{self.prefix}_leg_controls"
        self.control_shape: Curve = Curve()

    def create_leg_ik(self):
        self.create_leg_ik_joints()
        self.create_leg_ik_controls()
        self.create_knee_space_swap()

    def create_leg_ik_joints(self):
        if not cmds.objExists(self.kinematic_parent_group):
            cmds.group(empty=True, name=self.kinematic_parent_group)
            cmds.parent(self.kinematic_parent_group, "rig_systems")

        previous_ik_joint = self.kinematic_parent_group
        for count, joint in enumerate(self.leg_segments):
            current_ik_joint = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_IK")[0]
            cmds.parentConstraint(current_ik_joint, joint, maintainOffset=True)
            cmds.parent(current_ik_joint, previous_ik_joint)

            bake_transform_to_offset_parent_matrix(current_ik_joint)

            previous_ik_joint = current_ik_joint

    def create_leg_ik_controls(self):
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        ik_leg_ctrl = self.control_shape.curve_four_way_arrow(name=f"{self.prefix}_leg_IK_CTRL")
        cmds.setAttr(f"{ik_leg_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)

        ik_knee_ctrl = self.control_shape.curve_triangle(name=f"{self.prefix}_knee_IK_CTRL")
        cmds.setAttr(f"{ik_knee_ctrl}.rotateOrder", RotateOrder[self.rotation_order].value)

        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_leg",
            startJoint=f"{self.leg_segments[0]}_IK",
            endEffector=f"{self.leg_segments[-3]}_IK",
            solver="ikRPsolver")[0]

        # ANKLE
        cmds.matchTransform(ik_leg_ctrl, f"{self.leg_segments[-3]}_IK", position=True, rotation=True, scale=False)
        cmds.parent(ik_handle, ik_leg_ctrl)
        cmds.orientConstraint(ik_leg_ctrl, f"{self.leg_segments[-3]}_IK", maintainOffset=True)
        cmds.parent(ik_leg_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_leg_ctrl)

        # POLE
        cmds.matchTransform(ik_knee_ctrl, f"{self.leg_segments[1]}_IK", position=True, rotation=False, scale=False)
        cmds.rotate(90, 0, 0, ik_knee_ctrl, relative=True)
        position = cmds.xform(ik_knee_ctrl, query=True, translation=True, worldSpace=True)
        cmds.move(position[0], position[1], position[2] + 75, ik_knee_ctrl)
        cmds.poleVectorConstraint(ik_knee_ctrl, ik_handle)
        cmds.parent(ik_knee_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_knee_ctrl)

    def create_knee_space_swap(self):

        cmds.addAttr(f"{self.prefix}_knee_IK_CTRL", attributeType="enum", enumName=f"WORLD=0:FOOT=1",
                     niceName="KNEE_FOLLOW",
                     longName="KNEE_FOLLOW", defaultValue=0, keyable=True)

        knee_space_swap = cmds.createNode("blendMatrix", name=f"{self.prefix}_blend_matrix_knee_space_swap")
        offset_matrix = cmds.getAttr(f"{self.prefix}_knee_IK_CTRL.offsetParentMatrix")
        cmds.setAttr(f"{knee_space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_leg_swap_position = cmds.spaceLocator(name=f"{self.prefix}_ik_leg_swap_position")
        cmds.matchTransform(ik_leg_swap_position, f"{self.prefix}_knee_IK_CTRL", position=True, rotation=True,
                            scale=False)
        cmds.parent(ik_leg_swap_position, f"{self.prefix}_leg_IK_CTRL")

        bake_transform_to_offset_parent_matrix(ik_leg_swap_position[0])

        cmds.connectAttr(f"{ik_leg_swap_position[0]}.worldMatrix[0]", f"{knee_space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{knee_space_swap}.outputMatrix", f"{self.prefix}_knee_IK_CTRL.offsetParentMatrix")
        cmds.connectAttr(f"{self.prefix}_knee_IK_CTRL.KNEE_FOLLOW", f"{knee_space_swap}.envelope")

        cmds.addAttr(f"{self.prefix}_leg_IK_CTRL", longName="KNEE_FOLLOW",
                     proxy=f"{self.prefix}_knee_IK_CTRL.KNEE_FOLLOW")
