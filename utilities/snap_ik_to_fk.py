import maya.cmds as cmds


def snap_ik_to_fk_limb(limb: str):
    match limb:
        case "Left Arm":
            snap_ik_to_fk_left_arm()
        case "Right Arm":
            snap_ik_to_fk_right_arm()
        case "Left Leg":
            snap_ik_to_fk_left_leg()
        case "Right Leg":
            snap_ik_to_fk_right_leg()
        case "All":
            snap_ik_to_fk_left_arm()
            snap_ik_to_fk_right_arm()
            snap_ik_to_fk_left_leg()
            snap_ik_to_fk_right_leg()


# Separate snap functions for re-usability
def snap_ik_to_fk_left_arm():
    cmds.matchTransform("L_IK_CTRL_arm", "L_FK_wrist", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_IK_CTRL_elbow", "L_LOC_elbow_position", position=True, rotation=True, scale=False)


def snap_ik_to_fk_right_arm():
    cmds.matchTransform("R_IK_CTRL_arm", "R_FK_wrist", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_IK_CTRL_elbow", "R_LOC_elbow_position", position=True, rotation=True, scale=False)


def snap_ik_to_fk_left_leg():
    cmds.matchTransform("L_IK_CTRL_leg", "L_LOC_ankle_position", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_IK_CTRL_knee", "L_LOC_knee_position", position=True, rotation=True, scale=False)


def snap_ik_to_fk_right_leg():
    cmds.matchTransform("R_IK_CTRL_leg", "R_LOC_ankle_position", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_IK_CTRL_knee", "R_LOC_knee_position", position=True, rotation=True, scale=False)


if __name__ == "__main__":
    pass
