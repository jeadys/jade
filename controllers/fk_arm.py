import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class FKArm:
    def __init__(self, prefix) -> None:
        self.prefix = prefix

    def create_fk_arm_control(self, control_name: str, connected_limb: str, pivot_from: str = None):
        fk_offset = cmds.group(empty=True, name=f"{self.prefix}_FK_OFFSET_{control_name}")

        fk_ctrl = ControlShape.curve_circle(name=f"{self.prefix}_FK_CTRL_{control_name}")[0]

        cmds.setAttr(f"{fk_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{fk_ctrl}.overrideColor", 12)

        cmds.parent(fk_ctrl, fk_offset)

        if pivot_from:
            cmds.matchTransform(fk_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=True,
                                scale=False)
            position_pivot = cmds.xform(f"{self.prefix}_DEF_{connected_limb}", query=True, translation=True,
                                        worldSpace=True)

            position_humerus = cmds.xform(f"{self.prefix}_DEF_humerus", query=True, translation=True, worldSpace=True)
            cmds.move(position_humerus[0], position_humerus[1], position_humerus[2], fk_offset)

            cmds.xform(fk_ctrl, pivots=[position_pivot[0], position_pivot[1], position_pivot[2]], worldSpace=True)
            cmds.xform(fk_offset, pivots=[position_pivot[0], position_pivot[1], position_pivot[2]], worldSpace=True)
        else:
            cmds.matchTransform(fk_offset, f"{self.prefix}_DEF_{connected_limb}", position=True, rotation=True,
                                scale=False)

        self.create_fk_arm_constraints(control_name=control_name, fk_ctrl=fk_ctrl, connected_limb=connected_limb)

        return fk_offset, fk_ctrl

    def create_fk_arm_joints(self):
        if not cmds.objExists(f"{self.prefix}_arm_group"):
            cmds.group(empty=True, name=f"{self.prefix}_arm_group")
            cmds.parent(f"{self.prefix}_arm_group", "rig_systems")

        fk_humerus = cmds.duplicate(f"{self.prefix}_DEF_humerus", parentOnly=True, name=f"{self.prefix}_FK_humerus")
        fk_radius = cmds.duplicate(f"{self.prefix}_DEF_radius", parentOnly=True, name=f"{self.prefix}_FK_radius")
        fk_wrist = cmds.duplicate(f"{self.prefix}_DEF_wrist", parentOnly=True, name=f"{self.prefix}_FK_wrist")

        cmds.parent(fk_humerus,  f"{self.prefix}_arm_group")
        cmds.parent(fk_radius, fk_humerus)
        cmds.parent(fk_wrist, fk_radius)

    def create_fk_arm_controls(self):
        self.create_fk_arm_joints()

        fk_offset_humerus, fk_ctrl_humerus = self.create_fk_arm_control(control_name="humerus",
                                                                        connected_limb="humerus")
        fk_offset_radius, fk_ctrl_radius = self.create_fk_arm_control(control_name="radius",
                                                                      connected_limb="radius")
        fk_offset_wrist, fk_ctrl_wrist = self.create_fk_arm_control(control_name="wrist", connected_limb="wrist")

        cmds.parent(fk_offset_humerus, f"{self.prefix}_arm_controls")
        cmds.parent(fk_offset_radius, fk_ctrl_humerus)
        cmds.parent(fk_offset_wrist, fk_ctrl_radius)

        if cmds.objExists("L_DEF_humerus") and cmds.objExists("FK_CTRL_spine_03") and not cmds.objExists("L_arm_group_FK"):
            cmds.group(empty=True, name="L_arm_group_FK")
            cmds.matchTransform("L_arm_group_FK", "L_DEF_humerus", position=True, rotation=True, scale=False)
            cmds.parent("L_arm_group_FK", "FK_CTRL_spine_03")
            cmds.parentConstraint("L_arm_group_FK", "L_FK_OFFSET_humerus", maintainOffset=True)
            cmds.parentConstraint("L_arm_group_FK", "L_arm_group", maintainOffset=True)

    def create_fk_arm_constraints(self, control_name: str, fk_ctrl, connected_limb) -> None:
        cmds.parentConstraint(fk_ctrl, f"{self.prefix}_FK_{connected_limb}", maintainOffset=True)
        cmds.parentConstraint(f"{self.prefix}_FK_{connected_limb}", f"{self.prefix}_DEF_{connected_limb}",
                              maintainOffset=True)


if __name__ == "__main__":
    pass
