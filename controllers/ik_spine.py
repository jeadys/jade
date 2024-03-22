import maya.cmds as cmds
from controllers.control_shape import ControlShape
from importlib import reload
import controllers.control_shape as control_shape

reload(control_shape)


class IKSpine:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_ik_spine_control(control_name: str, connected_limb: str, control_shape: str = "curve_circle"):
        ik_offset = cmds.group(empty=True, name=f"IK_OFFSET_{control_name}")

        match control_shape:
            case "curve_circle":
                ik_ctrl = ControlShape.curve_circle(name=f"IK_CTRL_{control_name}")[0]
            case "curve_cog":
                ik_ctrl = ControlShape.curve_cog(name=f"IK_CTRL_{control_name}")
            case "curve_star":
                ik_ctrl = ControlShape.curve_star(name=f"IK_CTRL_{control_name}")[0]
            case "curve_hip":
                ik_ctrl = ControlShape.curve_hip(name=f"IK_CTRL_{control_name}")[0]
            case "curve_pelvis":
                ik_ctrl = ControlShape.curve_pelvis(name=f"IK_CTRL_{control_name}")[0]
            case "curve_shoulder":
                ik_ctrl = ControlShape.curve_shoulder(name=f"IK_CTRL_{control_name}")[0]
            case _:
                ik_ctrl = ControlShape.curve_circle(name=f"IK_CTRL_{control_name}")[0]

        cmds.setAttr(f"{ik_ctrl}.overrideEnabled", 1)
        cmds.setAttr(f"{ik_ctrl}.overrideColor", 12)

        cmds.parent(ik_ctrl, ik_offset)

        cmds.matchTransform(ik_offset, connected_limb, position=True, rotation=False, scale=False)

        if control_name == "hip":
            # set hip offset lower than cog location
            position_hip = cmds.xform("IK_pelvis", query=True, translation=True, worldSpace=True)
            cmds.move(position_hip[0], position_hip[1] - 30, position_hip[2], ik_offset)

            # set hip ctrl pivot to pelvis location
            cmds.xform(ik_ctrl, pivots=[position_hip[0], position_hip[1], position_hip[2]], worldSpace=True)

        return ik_offset, ik_ctrl

    @staticmethod
    def create_ik_spine_joints():
        if not cmds.objExists("spine_group"):
            cmds.group(empty=True, name="spine_group")
            cmds.parent("spine_group", "rig_systems")

        ik_pelvis = cmds.duplicate("DEF_pelvis", parentOnly=True, name="IK_pelvis")
        ik_spine_one = cmds.duplicate("DEF_spine_01", parentOnly=True, name="IK_spine_01")
        ik_spine_two = cmds.duplicate("DEF_spine_02", parentOnly=True, name="IK_spine_02")
        ik_spine_three = cmds.duplicate("DEF_spine_03", parentOnly=True, name="IK_spine_03")
        ik_neck = cmds.duplicate("DEF_neck", parentOnly=True, name="IK_neck")

        cmds.parent(ik_pelvis, "spine_group")
        cmds.parent(ik_spine_one, ik_pelvis)
        cmds.parent(ik_spine_two, ik_spine_one)
        cmds.parent(ik_spine_three, ik_spine_two)
        cmds.parent(ik_neck, ik_spine_three)

        # Joints to control spine curve
        ik_pelvis_ctrl_joint = cmds.duplicate("DEF_pelvis", parentOnly=True, name="IK_pelvis_ctrl_joint")
        ik_mid_spine_ctrl_joint = cmds.duplicate("DEF_spine_02", parentOnly=True, name="IK_mid_spine_ctrl_joint")
        ik_upper_spine_ctrl_joint = cmds.duplicate("DEF_neck", parentOnly=True, name="IK_upper_spine_ctrl_joint")

        cmds.parent(ik_pelvis_ctrl_joint, world=True)
        cmds.parent(ik_mid_spine_ctrl_joint, world=True)
        cmds.parent(ik_upper_spine_ctrl_joint, world=True)

        cmds.joint(ik_pelvis_ctrl_joint, edit=True, orientJoint="none", zeroScaleOrient=True)
        cmds.joint(ik_mid_spine_ctrl_joint, edit=True, orientJoint="none", zeroScaleOrient=True)
        cmds.joint(ik_upper_spine_ctrl_joint, edit=True, orientJoint="none", zeroScaleOrient=True)

        cmds.setAttr(f"{ik_pelvis_ctrl_joint[0]}.radius", 5)
        cmds.setAttr(f"{ik_mid_spine_ctrl_joint[0]}.radius", 5)
        cmds.setAttr(f"{ik_upper_spine_ctrl_joint[0]}.radius", 5)

    def create_ik_spine_controls(self):
        self.create_ik_spine_joints()

        # CENTER SPINE
        ik_offset_cog, ik_ctrl_cog = self.create_ik_spine_control(control_name="cog",
                                                                  connected_limb="DEF_cog",
                                                                  control_shape="curve_cog")
        ik_offset_hip, ik_ctrl_hip = self.create_ik_spine_control(control_name="hip",
                                                                  connected_limb="IK_pelvis_ctrl_joint",
                                                                  control_shape="curve_hip")
        ik_offset_pelvis, ik_ctrl_pelvis = self.create_ik_spine_control(control_name="pelvis",
                                                                        connected_limb="IK_pelvis",
                                                                        control_shape="curve_pelvis")
        ik_offset_chest, ik_ctrl_chest = self.create_ik_spine_control(control_name="chest",
                                                                      connected_limb="IK_mid_spine_ctrl_joint",
                                                                      control_shape="curve_star")
        ik_offset_spine_shoulder, ik_ctrl_shoulder = self.create_ik_spine_control(control_name="shoulder",
                                                                                  connected_limb="IK_upper_spine_ctrl_joint",
                                                                                  control_shape="curve_shoulder")

        cmds.parent(ik_offset_cog, "spine_controls")
        cmds.parent(ik_offset_pelvis, ik_ctrl_cog)
        cmds.parent(ik_offset_hip, ik_ctrl_cog)
        cmds.parent(ik_offset_chest, ik_ctrl_pelvis)
        cmds.parent(ik_offset_spine_shoulder, ik_ctrl_chest)

        self.create_ik_spine_constraints()
        self.create_ik_spine_handle()
        self.create_ik_spine_arm_follow()

    @staticmethod
    def create_ik_spine_handle():
        # spine
        def_pelvis = cmds.ls("DEF_pelvis", type="joint")
        pelvis_position = cmds.xform(def_pelvis, query=True, translation=True, worldSpace=True)

        def_spine_one = cmds.ls("DEF_spine_01", type="joint")
        spine_one_position = cmds.xform(def_spine_one, query=True, translation=True, worldSpace=True)

        def_spine_two = cmds.ls("DEF_spine_02", type="joint")
        spine_two_position = cmds.xform(def_spine_two, query=True, translation=True, worldSpace=True)

        def_spine_three = cmds.ls("DEF_spine_03", type="joint")
        spine_three_position = cmds.xform(def_spine_three, query=True, translation=True, worldSpace=True)

        def_neck = cmds.ls("DEF_neck", type="joint")
        neck_position = cmds.xform(def_neck, query=True, translation=True, worldSpace=True)

        curve_spine = cmds.curve(
            name="curve_spine",
            point=[
                (pelvis_position[0], pelvis_position[1], pelvis_position[2]),
                (spine_one_position[0], spine_one_position[1], spine_one_position[2]),
                (spine_two_position[0], spine_two_position[1], spine_two_position[2]),
                (spine_three_position[0], spine_three_position[1], spine_three_position[2]),
                (neck_position[0], neck_position[1], neck_position[2]),
            ],
            # degree=1,
        )

        cmds.ikHandle(
            name="ikHandle_spine",
            startJoint="IK_pelvis",
            endEffector="IK_neck",
            solver="ikSplineSolver",
            curve=curve_spine,
            createCurve=False,
            parentCurve=False,
        )

        cmds.skinCluster(
            "IK_pelvis_ctrl_joint", "IK_mid_spine_ctrl_joint", "IK_upper_spine_ctrl_joint", curve_spine,
            maximumInfluences=5, bindMethod=0, skinMethod=0
        )

    @staticmethod
    def create_ik_spine_constraints():
        cmds.parentConstraint("IK_CTRL_cog", "DEF_cog", maintainOffset=True)
        cmds.parentConstraint("IK_pelvis", "DEF_pelvis", maintainOffset=True)
        cmds.parentConstraint("IK_spine_01", "DEF_spine_01", maintainOffset=True)
        cmds.parentConstraint("IK_spine_02", "DEF_spine_02", maintainOffset=True)
        cmds.parentConstraint("IK_spine_03", "DEF_spine_03", maintainOffset=True)
        cmds.parentConstraint("IK_neck", "DEF_neck", maintainOffset=True)

    @staticmethod
    def create_ik_spine_arm_follow():
        if cmds.objExists("L_DEF_humerus") and cmds.objExists("L_FK_OFFSET_humerus") and not cmds.objExists(
                "L_arm_group_IK"):
            cmds.group(empty=True, name="L_arm_group_IK")
            cmds.matchTransform("L_arm_group_IK", "L_DEF_humerus", position=True, rotation=True, scale=False)
            cmds.parent("L_arm_group_IK", "IK_CTRL_shoulder")
            cmds.parentConstraint("L_arm_group_IK", "L_FK_OFFSET_humerus", maintainOffset=True)
            cmds.parentConstraint("L_arm_group_IK", "L_arm_group", maintainOffset=True)


if __name__ == "__main__":
    pass
