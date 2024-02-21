import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape
import mechanisms.arm_stretch as arm_stretch_module

reload(control_shape)
reload(arm_stretch_module)


class IKArm:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_ik_arm_control(self, control_name: str, connected_limb: str):
        ik_offset = cmds.group(empty=True, name=f"{self.prefix}_IK_OFFSET_{control_name}")

        ik_ctrl = ControlShape.curve_wrist(name=f"{self.prefix}_IK_CTRL_{control_name}")

        cmds.setAttr(f"{ik_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{ik_ctrl}.overrideColor", 14)

        cmds.parent(ik_ctrl, ik_offset)

        match control_name:
            case "arm":
                self.create_ik_arm_handle()
                self.create_ik_arm(ik_offset=ik_offset, connected_limb=connected_limb)
                self.create_ik_arm_constraint(ik_ctrl=ik_ctrl)
            case "elbow":
                self.create_ik_elbow(ik_offset=ik_offset, connected_limb=connected_limb, control_name=control_name)
                self.create_ik_elbow_constraint(ik_ctrl=ik_ctrl)

        return ik_offset, ik_ctrl

    def create_ik_arm_handle(self):
        cmds.ikHandle(name=f"{self.prefix}_ikHandle_arm", startJoint=f"{self.prefix}_IK_humerus",
                      endEffector=f"{self.prefix}_IK_wrist", solver="ikRPsolver")

    def create_ik_arm(self, ik_offset, connected_limb):
        cmds.matchTransform(ik_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=True, scale=False)
        cmds.parent(f"{self.prefix}_ikHandle_arm", f"{self.prefix}_IK_CTRL_arm")

    def create_ik_arm_constraint(self, ik_ctrl):
        cmds.parentConstraint(f"{self.prefix}_IK_humerus", f"{self.prefix}_DEF_humerus", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_radius", f"{self.prefix}_DEF_radius", maintainOffset=False)
        cmds.parentConstraint(f"{self.prefix}_IK_wrist", f"{self.prefix}_DEF_wrist", maintainOffset=False)
        # wrist orientation
        cmds.orientConstraint(ik_ctrl, f"{self.prefix}_IK_wrist", maintainOffset=True)

    # ELBOW
    def create_ik_elbow(self, ik_offset, connected_limb, control_name):
        cmds.matchTransform(ik_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=False,
                            scale=False)
        position = cmds.xform(ik_offset, query=True, translation=True, worldSpace=True)
        cmds.rotate(90, 0, 0, ik_offset, relative=True)
        cmds.move(position[0], position[1], position[2] - 75, ik_offset)

        # IK > FK SNAP LOCATOR
        elbow_loc_position = cmds.spaceLocator(name=f"{self.prefix}_LOC_{control_name}_position")
        cmds.matchTransform(elbow_loc_position, f"{self.prefix}_IK_CTRL_{control_name}", position=True, rotation=True,
                            scale=False)
        cmds.scale(6, 6, 6, elbow_loc_position)
        cmds.parent(elbow_loc_position, f"{self.prefix}_FK_radius")

    def create_ik_elbow_constraint(self, ik_ctrl):
        cmds.poleVectorConstraint(ik_ctrl, f"{self.prefix}_ikHandle_arm")

    def create_ik_arm_joints(self):
        if not cmds.objExists(f"{self.prefix}_arm_group"):
            cmds.group(empty=True, name=f"{self.prefix}_arm_group")
            cmds.matchTransform(f"{self.prefix}_arm_group", f"{self.prefix}_DEF_humerus")
            cmds.parent(f"{self.prefix}_arm_group", "rig_systems")

        ik_humerus = cmds.duplicate(f"{self.prefix}_DEF_humerus", parentOnly=True, name=f"{self.prefix}_IK_humerus")
        ik_radius = cmds.duplicate(f"{self.prefix}_DEF_radius", parentOnly=True, name=f"{self.prefix}_IK_radius")
        ik_wrist = cmds.duplicate(f"{self.prefix}_DEF_wrist", parentOnly=True, name=f"{self.prefix}_IK_wrist")

        cmds.parent(ik_humerus, f"{self.prefix}_arm_group")
        cmds.parent(ik_radius, ik_humerus)
        cmds.parent(ik_wrist, ik_radius)

    def create_ik_arm_controls(self) -> None:
        self.create_ik_arm_joints()

        fk_offset_arm, _fk_ctrl_arm = self.create_ik_arm_control(control_name="arm", connected_limb="wrist")
        fk_offset_elbow, _fk_ctrl_elbow = self.create_ik_arm_control(control_name="elbow", connected_limb="radius")

        cmds.parent(fk_offset_arm, f"{self.prefix}_arm_controls")
        cmds.parent(fk_offset_elbow, f"{self.prefix}_arm_controls")

        if cmds.objExists("L_DEF_humerus") and cmds.objExists("IK_CTRL_shoulder") and not cmds.objExists("L_arm_group_IK"):
            cmds.group(empty=True, name="L_arm_group_IK")
            cmds.matchTransform("L_arm_group_IK", "L_DEF_humerus", position=True, rotation=True, scale=False)
            cmds.parent("L_arm_group_IK", "IK_CTRL_shoulder")
            cmds.parentConstraint("L_arm_group_IK", "L_FK_OFFSET_humerus", maintainOffset=True)
            cmds.parentConstraint("L_arm_group_IK", "L_arm_group", maintainOffset=True)


if __name__ == "__main__":
    pass
