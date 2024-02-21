import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class FKSpine:
    def __init__(self) -> None:
        pass

    def create_fk_spine_control(self, control_name: str, connected_limb: str, control_shape: str = "curve_circle"):
        fk_offset = cmds.group(empty=True, name=f"FK_OFFSET_{control_name}")

        match control_shape:
            case "curve_circle":
                fk_ctrl = ControlShape.curve_circle(name=f"FK_CTRL_{control_name}")[0]
            case "curve_cog":
                fk_ctrl = ControlShape.curve_cog(name=f"FK_CTRL_{control_name}")
            case "curve_star":
                fk_ctrl = ControlShape.curve_star(name=f"FK_CTRL_{control_name}")[0]
            case "curve_waist":
                fk_ctrl = ControlShape.curve_waist(name=f"FK_CTRL_{control_name}")[0]
            case _:
                fk_ctrl = ControlShape.curve_circle(name=f"FK_CTRL_{control_name}")[0]

        cmds.setAttr(f"{fk_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{fk_ctrl}.overrideColor", 12)

        cmds.parent(fk_ctrl, fk_offset)

        cmds.matchTransform(fk_offset, f"DEF_{connected_limb}", position=True, rotation=True, scale=False)

        self.create_fk_spine_constraints(fk_ctrl=fk_ctrl, connected_limb=connected_limb)

        return fk_offset, fk_ctrl

    @staticmethod
    def create_fk_spine_joints():
        if not cmds.objExists("spine_group"):
            cmds.group(empty=True, name="spine_group")
            cmds.parent("spine_group", "rig_systems")

        fk_pelvis = cmds.duplicate("DEF_pelvis", parentOnly=True, name="FK_pelvis")
        fk_spine_one = cmds.duplicate("DEF_spine_01", parentOnly=True, name="FK_spine_01")
        fk_spine_two = cmds.duplicate("DEF_spine_02", parentOnly=True, name="FK_spine_02")
        fk_spine_three = cmds.duplicate("DEF_spine_03", parentOnly=True, name="FK_spine_03")
        fk_neck = cmds.duplicate("DEF_neck", parentOnly=True, name="FK_neck")

        cmds.parent(fk_pelvis, "spine_group")
        cmds.parent(fk_spine_one, fk_pelvis)
        cmds.parent(fk_spine_two, fk_spine_one)
        cmds.parent(fk_spine_three, fk_spine_two)
        cmds.parent(fk_neck, fk_spine_three)

    def create_fk_spine_controls(self):
        self.create_fk_spine_joints()

        # CENTER SPINE
        fk_offset_pelvis, fk_ctrl_pelvis = self.create_fk_spine_control(control_name="pelvis", connected_limb="pelvis")
        fk_offset_spine_one, fk_ctrl_spine_one = self.create_fk_spine_control(control_name="spine_01",
                                                                              connected_limb="spine_01")
        fk_offset_spine_two, fk_ctrl_spine_two = self.create_fk_spine_control(control_name="spine_02",
                                                                              connected_limb="spine_02")
        fk_offset_spine_three, fk_ctrl_spine_three = self.create_fk_spine_control(control_name="spine_03",
                                                                                  connected_limb="spine_03")
        fk_offset_neck, fk_ctrl_spine_neck = self.create_fk_spine_control(control_name="neck", connected_limb="neck")

        cmds.parent(fk_offset_pelvis, "spine_controls")
        cmds.parent(fk_offset_spine_one, fk_ctrl_pelvis)
        cmds.parent(fk_offset_spine_two, fk_ctrl_spine_one)
        cmds.parent(fk_offset_spine_three, fk_ctrl_spine_two)
        cmds.parent(fk_offset_neck, fk_ctrl_spine_three)

        self.create_ik_spine_arm_follow()

    @staticmethod
    def create_fk_spine_constraints(fk_ctrl, connected_limb) -> None:
        cmds.parentConstraint(fk_ctrl, f"FK_{connected_limb}", maintainOffset=True)
        cmds.parentConstraint(f"FK_{connected_limb}", f"DEF_{connected_limb}", maintainOffset=True)

    @staticmethod
    def create_ik_spine_arm_follow():
        if cmds.objExists("L_DEF_humerus") and cmds.objExists("L_FK_OFFSET_humerus") and not cmds.objExists(
                "L_arm_group_FK"):
            cmds.group(empty=True, name="L_arm_group_FK")
            cmds.matchTransform("L_arm_group_FK", "L_DEF_humerus", position=True, rotation=True, scale=False)
            cmds.parent("L_arm_group_FK", "FK_CTRL_spine_03")
            cmds.parentConstraint("L_arm_group_FK", "L_FK_OFFSET_humerus", maintainOffset=True)
            cmds.parentConstraint("L_arm_group_FK", "L_arm_group", maintainOffset=True)


if __name__ == "__main__":
    pass
