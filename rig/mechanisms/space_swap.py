import maya.cmds as cmds

from utilities.bake_transform import bake_transform_to_offset_parent_matrix


def inverse_kinematic_space_swap(ik_control, pole_control, component):
    cmds.addAttr(pole_control, attributeType="enum", enumName=f"world=0:{component}=1", niceName=f"follow", longName=f"follow",
                 defaultValue=0, keyable=True)

    cmds.addAttr(ik_control, longName=f"follow", proxy=f"{pole_control}.follow")

    space_swap = cmds.createNode("blendMatrix", name=f"{component}_blend_matrix_space_swap_#")
    offset_matrix = cmds.getAttr(f"{pole_control}.offsetParentMatrix")
    cmds.setAttr(f"{space_swap}.inputMatrix", offset_matrix, type="matrix")

    ik_swap_position = cmds.spaceLocator(name=f"{component}_ik_swap_position_#")[0]
    cmds.setAttr(f"{ik_swap_position}.visibility", False)
    cmds.matchTransform(ik_swap_position, pole_control, position=True, rotation=True, scale=False)
    cmds.parent(ik_swap_position, ik_control)

    bake_transform_to_offset_parent_matrix(ik_swap_position)

    cmds.connectAttr(f"{ik_swap_position}.worldMatrix[0]", f"{space_swap}.target[0].targetMatrix")
    cmds.connectAttr(f"{space_swap}.outputMatrix", f"{pole_control}.offsetParentMatrix")
    cmds.connectAttr(f"{pole_control}.follow", f"{space_swap}.envelope")