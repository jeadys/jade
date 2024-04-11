import maya.cmds as cmds
from utilities.set_rgb_color import set_rgb_color
from utilities.bake_transform import bake_transform_to_offset_parent_matrix


def create_layer_joints(prefix: str, name: str, layer_name: str, segments: list[str]) -> list[str]:
    kinematic_parent_group: str = f"{prefix}_{name}_kinematics"

    if not cmds.objExists(kinematic_parent_group):
        cmds.group(empty=True, name=kinematic_parent_group)
        cmds.parent(kinematic_parent_group, "rig_systems")

    layer_joints: list[str] = []
    previous_layer_joint = kinematic_parent_group
    for index, joint in enumerate(segments):
        current_layer_joint: str = cmds.duplicate(joint, parentOnly=True, name=f"{joint}_{layer_name}")[0]
        cmds.parentConstraint(current_layer_joint, joint, maintainOffset=True)
        cmds.parent(current_layer_joint, previous_layer_joint)
        set_rgb_color(node=current_layer_joint, color=(1, 0, 1))

        bake_transform_to_offset_parent_matrix(current_layer_joint)

        layer_joints.append(current_layer_joint)
        previous_layer_joint = current_layer_joint

    return layer_joints
