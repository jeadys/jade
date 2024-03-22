import maya.cmds as cmds


def snap_fk_to_ik_limb(limb: str):
    match limb:
        case "Left Arm":
            snap_fk_to_ik_left_arm()
        case "Right Arm":
            snap_fk_to_ik_right_arm()
        case "Left Leg":
            snap_fk_to_ik_left_leg()
        case "Right Leg":
            snap_fk_to_ik_right_leg()
        case "All":
            snap_fk_to_ik_left_arm()
            snap_fk_to_ik_right_arm()
            snap_fk_to_ik_left_leg()
            snap_fk_to_ik_right_leg()


# Separate snap functions for re-usability
def snap_fk_to_ik_left_arm():
    cmds.matchTransform("L_FK_CTRL_humerus", "L_IK_humerus", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_radius", "L_IK_radius", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_wrist", "L_IK_wrist", position=True, rotation=True, scale=False)


def snap_fk_to_ik_right_arm():
    cmds.matchTransform("R_FK_CTRL_humerus", "R_IK_humerus", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_radius", "R_IK_radius", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_wrist", "R_IK_wrist", position=True, rotation=True, scale=False)


def snap_fk_to_ik_left_leg():
    cmds.matchTransform("L_FK_CTRL_femur", "L_IK_femur", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_tibia", "L_IK_tibia", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_ankle", "L_IK_ankle", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_ball", "L_IK_ball", position=True, rotation=True, scale=False)
    cmds.matchTransform("L_FK_CTRL_ball_end", "L_IK_ball_end", position=True, rotation=True, scale=False)


def snap_fk_to_ik_right_leg():
    cmds.matchTransform("R_FK_CTRL_femur", "R_IK_femur", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_tibia", "R_IK_tibia", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_ankle", "R_IK_ankle", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_ball", "R_IK_ball", position=True, rotation=True, scale=False)
    cmds.matchTransform("R_FK_CTRL_ball_end", "R_IK_ball_end", position=True, rotation=True, scale=False)


if __name__ == "__main__":
    pass
