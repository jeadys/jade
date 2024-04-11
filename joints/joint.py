import maya.cmds as cmds
from utilities.set_rgb_color import set_rgb_color


def create_joints(segments: list[str], rotation_order: str) -> list[str]:
    arm_joints_exist: bool = any(cmds.objExists(f"{joint}") for joint in segments)
    joint_parent_group: str = "skeleton"

    if arm_joints_exist:
        cmds.error(f"joints already exist in {joint_parent_group}")

    if not cmds.objExists(joint_parent_group):
        cmds.group(empty=True, name=joint_parent_group)

    joints: list[str] = []
    previous_joint: str = joint_parent_group
    for index, joint in enumerate(segments):
        # Prevent Maya from auto parenting joint to selected item in scene.
        cmds.select(deselect=True)
        current_joint = cmds.joint(radius=1, rotationOrder=rotation_order, name=f"{joint}")
        set_rgb_color(node=current_joint, color=(0, 1, 1))

        cmds.matchTransform(current_joint, f"{joint}_LOC", position=True, rotation=False, scale=False)
        cmds.parent(current_joint, previous_joint)

        joints.append(current_joint)
        previous_joint = current_joint

    return joints
