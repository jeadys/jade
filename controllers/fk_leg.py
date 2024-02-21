import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class FKLeg:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_fk_arm_control(self, control_name: str, connected_limb: str):
        fk_offset = cmds.group(empty=True, name=f"{self.prefix}_FK_OFFSET_{control_name}")

        fk_ctrl = ControlShape.curve_circle(name=f"{self.prefix}_FK_CTRL_{control_name}")[0]

        cmds.setAttr(f"{fk_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{fk_ctrl}.overrideColor", 12)

        cmds.parent(fk_ctrl, fk_offset)

        cmds.matchTransform(fk_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=True, scale=False)

        self.create_fk_arm_constraints(fk_ctrl=fk_ctrl, connected_limb=connected_limb)

        return fk_offset, fk_ctrl

    def create_fk_arm_joints(self):
        if not cmds.objExists(f"{self.prefix}_leg_group"):
            cmds.group(empty=True, name=f"{self.prefix}_leg_group")
            cmds.parent(f"{self.prefix}_leg_group", "rig_systems")

        fk_femur = cmds.duplicate(f"{self.prefix}_DEF_femur", parentOnly=True, name=f"{self.prefix}_FK_femur")
        fk_tibia = cmds.duplicate(f"{self.prefix}_DEF_tibia", parentOnly=True, name=f"{self.prefix}_FK_tibia")
        fk_ankle = cmds.duplicate(f"{self.prefix}_DEF_ankle", parentOnly=True, name=f"{self.prefix}_FK_ankle")
        fk_ball = cmds.duplicate(f"{self.prefix}_DEF_ball", parentOnly=True, name=f"{self.prefix}_FK_ball")
        fk_ball_end = cmds.duplicate(f"{self.prefix}_DEF_ball_end", parentOnly=True, name=f"{self.prefix}_FK_ball_end")

        cmds.parent(fk_femur, f"{self.prefix}_leg_group")
        cmds.parent(fk_tibia, fk_femur)
        cmds.parent(fk_ankle, fk_tibia)
        cmds.parent(fk_ball, fk_ankle)
        cmds.parent(fk_ball_end, fk_ball)

    def create_fk_arm_controls(self):
        self.create_fk_arm_joints()

        fk_offset_femur, fk_ctrl_femur = self.create_fk_arm_control(control_name="femur", connected_limb="femur")
        fk_offset_tibia, fk_ctrl_tibia = self.create_fk_arm_control(control_name="tibia", connected_limb="tibia")
        fk_offset_ankle, fk_ctrl_ankle = self.create_fk_arm_control(control_name="ankle", connected_limb="ankle")
        fk_offset_ball, fk_ctrl_ball = self.create_fk_arm_control(control_name="ball", connected_limb="ball")
        fk_offset_ball_end, fk_ctrl_ball_end = self.create_fk_arm_control(control_name="ball_end",
                                                                          connected_limb="ball_end")

        cmds.parent(fk_offset_femur, f"{self.prefix}_leg_controls")
        cmds.parent(fk_offset_tibia, fk_ctrl_femur)
        cmds.parent(fk_offset_ankle, fk_ctrl_tibia)
        cmds.parent(fk_offset_ball, fk_ctrl_ankle)
        cmds.parent(fk_offset_ball_end, fk_ctrl_ball)

    def create_fk_arm_constraints(self, fk_ctrl, connected_limb) -> None:
        cmds.parentConstraint(fk_ctrl, f"{self.prefix}_FK_{connected_limb}", maintainOffset=True)
        cmds.parentConstraint(f"{self.prefix}_FK_{connected_limb}", f"{self.prefix}_DEF_{connected_limb}",
                              maintainOffset=True)


if __name__ == "__main__":
    pass
