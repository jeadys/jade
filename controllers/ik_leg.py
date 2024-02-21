import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class IKLeg:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_ik_leg_control(self, control_name: str, connected_limb: str):
        ik_offset = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_{control_name}")

        ik_ctrl = ControlShape.curve_wrist(name=f"{self.prefix}_IK_CTRL_{control_name}")

        cmds.setAttr(f"{ik_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{ik_ctrl}.overrideColor", 14)

        cmds.parent(ik_ctrl, ik_offset)

        match control_name:
            case "leg":
                self.create_ik_leg_handle()
                self.create_ik_leg(ik_offset=ik_offset, connected_limb=connected_limb, control_name=control_name)
                self.create_ik_leg_constraint(ik_ctrl=ik_ctrl)
            case "knee":
                self.create_ik_knee(ik_offset=ik_offset, connected_limb=connected_limb, control_name=control_name)
                self.create_ik_knee_constraint(ik_ctrl=ik_ctrl)

        return ik_offset, ik_ctrl

    # LEG
    def create_ik_leg_handle(self):
        cmds.ikHandle(name=f"{self.prefix}_ikHandle_leg", startJoint=f"{self.prefix}_IK_femur",
                      endEffector=f"{self.prefix}_IK_ankle", solver="ikRPsolver")

    def create_ik_leg(self, ik_offset, connected_limb, control_name):
        cmds.matchTransform(ik_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=False,
                            scale=False)
        cmds.parent(f"{self.prefix}_ikHandle_leg", f"{self.prefix}_IK_CTRL_leg")

        # IK > FK SNAP LOCATOR
        ankle_loc_position = cmds.spaceLocator(name=f"{self.prefix}_LOC_{connected_limb}_position")
        cmds.matchTransform(ankle_loc_position, f"{self.prefix}_IK_CTRL_{control_name}", position=True, rotation=True,
                            scale=False)
        cmds.scale(6, 6, 6, ankle_loc_position)
        cmds.parent(ankle_loc_position, f"{self.prefix}_FK_ankle")

    def create_ik_leg_constraint(self, ik_ctrl):
        cmds.parentConstraint(f"{self.prefix}_IK_femur", f"{self.prefix}_DEF_femur", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_tibia", f"{self.prefix}_DEF_tibia", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_ankle", f"{self.prefix}_DEF_ankle", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_ball", f"{self.prefix}_DEF_ball", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_ball_end", f"{self.prefix}_DEF_ball_end", maintainOffset=False)
        # ankle orientation
        cmds.orientConstraint(ik_ctrl, f"{self.prefix}_IK_ankle", maintainOffset=True)

    # KNEE
    def create_ik_knee(self, ik_offset, connected_limb, control_name):
        cmds.matchTransform(ik_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=False,
                            scale=False)
        position = cmds.xform(ik_offset, query=True, translation=True, worldSpace=True)
        cmds.rotate(90, 0, 0, ik_offset, relative=True)
        cmds.move(position[0], position[1], position[2] + 75, ik_offset)

        # IK > FK SNAP LOCATOR
        knee_loc_position = cmds.spaceLocator(name=f"{self.prefix}_LOC_{control_name}_position")
        cmds.matchTransform(knee_loc_position, f"{self.prefix}_IK_CTRL_{control_name}", position=True, rotation=True,
                            scale=False)
        cmds.scale(6, 6, 6, knee_loc_position)
        cmds.parent(knee_loc_position, f"{self.prefix}_FK_tibia")

    def create_ik_knee_constraint(self, ik_ctrl):
        cmds.poleVectorConstraint(ik_ctrl, f"{self.prefix}_ikHandle_leg")

    def create_ik_leg_joints(self):
        if not cmds.objExists(f"{self.prefix}_leg_group"):
            cmds.group(empty=True, name=f"{self.prefix}_leg_group")
            cmds.parent(f"{self.prefix}_leg_group", "rig_systems")

        ik_femur = cmds.duplicate(f"{self.prefix}_DEF_femur", parentOnly=True, name=f"{self.prefix}_IK_femur")
        ik_tibia = cmds.duplicate(f"{self.prefix}_DEF_tibia", parentOnly=True, name=f"{self.prefix}_IK_tibia")
        ik_ankle = cmds.duplicate(f"{self.prefix}_DEF_ankle", parentOnly=True, name=f"{self.prefix}_IK_ankle")
        ik_ball = cmds.duplicate(f"{self.prefix}_DEF_ball", parentOnly=True, name=f"{self.prefix}_IK_ball")
        ik_ball_end = cmds.duplicate(f"{self.prefix}_DEF_ball_end", parentOnly=True, name=f"{self.prefix}_IK_ball_end")

        cmds.parent(ik_femur, f"{self.prefix}_leg_group")
        cmds.parent(ik_tibia, ik_femur)
        cmds.parent(ik_ankle, ik_tibia)
        cmds.parent(ik_ball, ik_ankle)
        cmds.parent(ik_ball_end, ik_ball)

    def create_ik_leg_controls(self) -> None:
        self.create_ik_leg_joints()

        fk_offset_leg, _fk_ctrl_leg = self.create_ik_leg_control(control_name="leg", connected_limb="ankle")
        fk_offset_knee, _fk_ctrl_knee = self.create_ik_leg_control(control_name="knee", connected_limb="tibia")

        cmds.parent(fk_offset_leg, f"{self.prefix}_leg_controls")
        cmds.parent(fk_offset_knee, f"{self.prefix}_leg_controls")


if __name__ == "__main__":
    pass
