import maya.cmds as cmds

from joints.joint_layer import create_layer_joints

from utilities.curve import Curve
from utilities.enums import RotateOrder
from utilities.set_rgb_color import set_rgb_color
from utilities.bake_transform import bake_transform_to_offset_parent_matrix


class IKChain:
    def __init__(self, prefix: str, name: str):
        self.prefix = prefix
        self.name = name
        self.kinematic_parent_group: str = f"{self.prefix}_{self.name}_kinematics"
        self.control_parent_group: str = f"{self.prefix}_{self.name}_controls"
        self.curve: Curve = Curve()

    def create_ik_joints(self, segments) -> list[str]:
        ik_joints: list[str] = create_layer_joints(prefix=self.prefix, name=self.name, layer_name="IK", segments=segments)

        return ik_joints

    def create_ik_controls(self, segments: list[str], rotation_order: str, name: str, scale: float) -> list[str]:
        if not cmds.objExists(self.control_parent_group):
            cmds.group(empty=True, name=self.control_parent_group)
            cmds.parent(self.control_parent_group, "controls")

        ik_ctrl = self.curve.curve_four_way_arrow(name=f"{self.prefix}_{name}_IK_CTRL", scale=scale)
        cmds.setAttr(f"{ik_ctrl}.rotateOrder", RotateOrder[rotation_order].value)
        set_rgb_color(node=ik_ctrl, color=(1, 0, 1))

        ik_pole_ctrl = self.curve.curve_cube(name=f"{self.prefix}_{name}_pole_IK_CTRL", scale=scale)
        cmds.setAttr(f"{ik_pole_ctrl}.rotateOrder", RotateOrder[rotation_order].value)
        set_rgb_color(node=ik_pole_ctrl, color=(0, 1, 1))

        ik_handle = cmds.ikHandle(
            name=f"{self.prefix}_ikHandle_{name}",
            startJoint=f"{segments[0]}",
            endEffector=f"{segments[-1]}",
            solver="ikRPsolver")[0]

        cmds.matchTransform(ik_ctrl, f"{segments[-1]}", position=True, rotation=True, scale=False)
        cmds.parent(ik_handle, ik_ctrl)
        cmds.orientConstraint(ik_ctrl, f"{segments[-1]}", maintainOffset=True)
        cmds.parent(ik_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_ctrl)

        cmds.matchTransform(ik_pole_ctrl, f"{segments[1]}", position=True, rotation=False, scale=False)
        cmds.rotate(90, 0, 0, ik_pole_ctrl, relative=True)
        position = cmds.xform(ik_pole_ctrl, query=True, translation=True, worldSpace=True)
        cmds.move(position[0], position[1], position[2], ik_pole_ctrl)
        cmds.poleVectorConstraint(ik_pole_ctrl, ik_handle)
        cmds.parent(ik_pole_ctrl, self.control_parent_group)

        bake_transform_to_offset_parent_matrix(ik_pole_ctrl)
        self.create_space_swap(ik_ctrl, ik_pole_ctrl)

        return [ik_ctrl, ik_pole_ctrl]

    def create_space_swap(self, ik_ctrl, ik_pole_ctrl):
        cmds.addAttr(ik_pole_ctrl, attributeType="enum", enumName=f"world=0:{self.name}=1",
                     niceName=f"{self.name}_follow",
                     longName=f"{self.name}_follow", defaultValue=0, keyable=True)

        cmds.addAttr(ik_ctrl, longName=f"{self.name}_follow", proxy=f"{ik_pole_ctrl}.{self.name}_follow")

        space_swap = cmds.createNode("blendMatrix", name=f"{self.prefix}_blend_matrix_{self.name}_space_swap")
        offset_matrix = cmds.getAttr(f"{ik_pole_ctrl}.offsetParentMatrix")
        cmds.setAttr(f"{space_swap}.inputMatrix", offset_matrix, type="matrix")

        ik_swap_position = cmds.spaceLocator(name=f"{self.prefix}_ik_{self.name}_swap_position")[0]
        cmds.setAttr(f"{ik_swap_position}.visibility", False)
        cmds.matchTransform(ik_swap_position, ik_pole_ctrl, position=True, rotation=True, scale=False)
        cmds.parent(ik_swap_position, ik_ctrl)

        bake_transform_to_offset_parent_matrix(ik_swap_position)

        cmds.connectAttr(f"{ik_swap_position}.worldMatrix[0]", f"{space_swap}.target[0].targetMatrix")
        cmds.connectAttr(f"{space_swap}.outputMatrix", f"{ik_pole_ctrl}.offsetParentMatrix")
        cmds.connectAttr(f"{ik_pole_ctrl}.{self.name}_follow", f"{space_swap}.envelope")
