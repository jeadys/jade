import maya.cmds as cmds
from importlib import reload

# Arm
import controllers.fk_arm as fk_arm_module
import controllers.ik_arm as ik_arm_module
import controllers.switch_arm as switch_arm_module
import mechanisms.arm_stretch as arm_stretch_module

# Leg
import controllers.fk_leg as fk_leg_module
import controllers.ik_leg as ik_leg_module
import controllers.switch_leg as switch_leg_module
import mechanisms.leg_stretch as leg_stretch_module

# Spine
import controllers.fk_spine as fk_spine_module
import controllers.ik_spine as ik_spine_module
import controllers.switch_spine as switch_spine_module
import mechanisms.spine_roll as spine_roll_module
import mechanisms.spine_stretch as spine_stretch_module

# Joints
import joints.arm as arm_module
import joints.leg as leg_module
import joints.spine as spine_module

import utilities.snap_fk_to_ik as snap_fk_to_ik_module
import utilities.snap_ik_to_fk as snap_ik_to_fk_module

import mechanisms.foot_roll as foot_roll_module

reload(arm_module)
reload(fk_arm_module)
reload(ik_arm_module)
reload(switch_arm_module)
reload(arm_stretch_module)

reload(leg_module)
reload(fk_leg_module)
reload(ik_leg_module)
reload(switch_leg_module)
reload(leg_stretch_module)

reload(spine_module)
reload(fk_spine_module)
reload(ik_spine_module)
reload(switch_spine_module)
reload(spine_roll_module)
reload(spine_stretch_module)

reload(snap_fk_to_ik_module)
reload(snap_ik_to_fk_module)

reload(foot_roll_module)


class MainWindow:
    def __init__(self):
        self.main_window = None
        self.limb_option_menu = None
        self.snap_option_menu = None
        self.window_name = "Rigger"

        # Check if the window already exists and close it
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)

        self.create_window()

    @staticmethod
    def update_checkboxes(*_args):
        selected_option = cmds.optionMenu("limb_option_menu", query=True, value=True)

        match selected_option:
            case "Arm":
                cmds.checkBox("is_roll_limb", edit=True, enable=True)
                cmds.checkBox("is_stretch_limb", edit=True, enable=True)
            case "Leg":
                cmds.checkBox("is_roll_limb", edit=True, enable=True)
                cmds.checkBox("is_stretch_limb", edit=True, enable=True)
            case "Spine":
                cmds.checkBox("is_roll_limb", edit=True, enable=True)
                cmds.checkBox("is_stretch_limb", edit=True, enable=True)

    def create_window(self):
        self.main_window = cmds.window(self.window_name, title=self.window_name, widthHeight=(450, 300), sizeable=False)
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

        # Create an optionMenu control
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=(2, 3))

        self.limb_option_menu = cmds.optionMenu("limb_option_menu", label="Select Limb:",
                                                changeCommand=self.update_checkboxes)
        cmds.menuItem(label="Left Arm")
        cmds.menuItem(label="Right Arm")
        cmds.menuItem(label="Left Leg")
        cmds.menuItem(label="Right Leg")
        cmds.menuItem(label="Spine")

        cmds.button(label="Add Locator", command=self.create_locator_button)
        cmds.button(label="Add Limb", command=self.create_joint_button)
        cmds.setParent(main_layout)

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=(1, 2, 3))
        cmds.checkBox("is_auto_parent", label="Auto Parent Limb", value=True)
        cmds.checkBox("is_roll_limb", label="Roll Limb", value=True)
        cmds.checkBox("is_stretch_limb", label="Stretch Limb", value=True)
        cmds.setParent(main_layout)

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=(1, 2, 3))
        cmds.button(label="Mirror Joints", command=cmds.MirrorJointOptions)
        cmds.button(label="Orient Joints", command=cmds.OrientJointOptions)
        cmds.button(label="Bind Skin", command=cmds.SmoothBindSkinOptions)
        cmds.setParent(main_layout)

        cmds.rowLayout(numberOfColumns=3, adjustableColumn=3)

        cmds.checkBox("is_ik_limb", label="IK Limb", value=True)
        cmds.checkBox("is_fk_limb", label="FK Limb", value=True)
        cmds.button(label="Generate Rig", height=50, command=self.generate_rig_button)
        cmds.setParent(main_layout)

        # Create an optionMenu control
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=(2, 3))
        self.snap_option_menu = cmds.optionMenu(label="Snap Limb:")
        cmds.menuItem(label="Left Arm")
        cmds.menuItem(label="Right Arm")
        cmds.menuItem(label="Left Leg")
        cmds.menuItem(label="Right Leg")
        cmds.menuItem(label="All")

        cmds.button(label="Snap IK > FK", command=self.snap_ik_to_fk_button)
        cmds.button(label="Snap FK > IK", command=self.snap_fk_to_ik_button)
        cmds.setParent(main_layout)

        cmds.showWindow(self.main_window)

    def snap_ik_to_fk_button(self, *_args):
        selected_item = cmds.optionMenu(self.snap_option_menu, query=True, value=True)
        snap_ik_to_fk_module.snap_ik_to_fk_limb(selected_item)

    def snap_fk_to_ik_button(self, *_args):
        selected_item = cmds.optionMenu(self.snap_option_menu, query=True, value=True)
        snap_fk_to_ik_module.snap_fk_to_ik_limb(selected_item)

    def create_locator_button(self, *_args):
        selected_item = cmds.optionMenu(self.limb_option_menu, query=True, value=True)

        match selected_item:
            case "Left Arm":
                arm_instance = arm_module.Arm(prefix="L")
                arm_instance.create_arm_locators()
            case "Right Arm":
                arm_instance = arm_module.Arm(prefix="R")
                arm_instance.create_arm_locators()
            case "Left Leg":
                leg_instance = leg_module.Leg(prefix="L")
                leg_instance.create_leg_locators()
            case "Right Leg":
                leg_instance = leg_module.Leg(prefix="R")
                leg_instance.create_leg_locators()
            case "Spine":
                spine_instance = spine_module.Spine()
                spine_instance.create_spine_locators()

    def create_joint_button(self, *_args):
        selected_item = cmds.optionMenu(self.limb_option_menu, query=True, value=True)
        is_auto_parent = cmds.checkBox("is_auto_parent", query=True, value=True)
        is_roll_limb = cmds.checkBox("is_roll_limb", query=True, value=True)

        match selected_item:
            case "Left Arm":
                arm_instance = arm_module.Arm(prefix="L")
                arm_instance.create_arm_joints(is_auto_parent, is_roll_limb)
            case "Right Arm":
                arm_instance = arm_module.Arm(prefix="R")
                arm_instance.create_arm_joints(is_auto_parent, is_roll_limb)
            case "Left Leg":
                leg_instance = leg_module.Leg(prefix="L")
                leg_instance.create_leg_joints(is_auto_parent, is_roll_limb)
            case "Right Leg":
                leg_instance = leg_module.Leg(prefix="R")
                leg_instance.create_leg_joints(is_auto_parent, is_roll_limb)
            case "Spine":
                spine_instance = spine_module.Spine()
                spine_instance.create_spine_joints(is_auto_parent)

    @staticmethod
    def generate_rig_button(*_args):
        is_stretch_limb = cmds.checkBox("is_stretch_limb", query=True, value=True)
        is_roll_limb = cmds.checkBox("is_roll_limb", query=True, value=True)

        if not cmds.objExists("controls"):
            cmds.group(empty=True, name="controls")

        if not cmds.objExists("DO_NOT_TOUCH"):
            cmds.group(empty=True, name="DO_NOT_TOUCH")

        if not cmds.objExists("geometries"):
            cmds.group(empty=True, name="geometries")
            cmds.parent("geometries", "DO_NOT_TOUCH")

        if not cmds.objExists("visual_aids"):
            cmds.group(empty=True, name="visual_aids")
            cmds.parent("visual_aids", "DO_NOT_TOUCH")

        if not cmds.objExists("rig_systems"):
            cmds.group(empty=True, name="rig_systems")
            cmds.parent("rig_systems", "DO_NOT_TOUCH")

        if cmds.objExists("L_DEF_clavicle") and cmds.objExists("L_DEF_upperarm") and cmds.objExists(
                "L_DEF_lowerarm") and cmds.objExists("L_DEF_wrist") and not cmds.objExists("L_arm_kinematics"):

            # FK ARM
            fk_arm_instance = fk_arm_module.FKArm(prefix="L")
            fk_arm_instance.create_fk_arm_joints()
            fk_arm_instance.create_fk_arm_controls()

            # IK ARM
            ik_arm_instance = ik_arm_module.IKArm(prefix="L")
            ik_arm_instance.create_ik_arm_joints()
            ik_arm_instance.create_ik_arm_controls()
            ik_arm_instance.create_elbow_space_swap()
            #
            # # SWITCH ARM
            # switch_arm_instance = switch_arm_module.SwitchArm(prefix="L")
            # switch_arm_instance.create_ik_fk_switch_arm_controls()
            #
            # # STRETCH ARM
            # if is_stretch_limb:
            #     arm_stretch_instance = arm_stretch_module.ArmStretch(prefix="L")
            #     arm_stretch_instance.create_arm_stretch_locators()
            #     arm_stretch_instance.create_arm_stretch_joints()
            #     arm_stretch_instance.create_arm_stretch_attributes()
            #     arm_stretch_instance.create_arm_stretch_nodes()

        if cmds.objExists("R_DEF_clavicle") and cmds.objExists("R_DEF_upperarm") and cmds.objExists(
                "R_DEF_lowerarm") and cmds.objExists("R_DEF_wrist") and not cmds.objExists("R_arm_kinematics"):

            # FK ARM
            fk_arm_instance = fk_arm_module.FKArm(prefix="R")
            fk_arm_instance.create_fk_arm_joints()
            fk_arm_instance.create_fk_arm_controls()

            # IK ARM
            ik_arm_instance = ik_arm_module.IKArm(prefix="R")
            ik_arm_instance.create_ik_arm_joints()
            ik_arm_instance.create_ik_arm_controls()
            ik_arm_instance.create_elbow_space_swap()
            #
            # # SWITCH ARM
            # switch_arm_instance = switch_arm_module.SwitchArm(prefix="L")
            # switch_arm_instance.create_ik_fk_switch_arm_controls()
            #
            # STRETCH ARM
            # if is_stretch_limb:
            #     arm_stretch_instance = arm_stretch_module.ArmStretch(prefix="R")
            #     arm_stretch_instance.create_arm_stretch_locators()
            #     arm_stretch_instance.create_arm_stretch_joints()
            #     arm_stretch_instance.create_arm_stretch_attributes()
            #     arm_stretch_instance.create_arm_stretch_nodes()

        if cmds.objExists("L_DEF_upperleg") and cmds.objExists("L_DEF_lowerleg") and cmds.objExists(
                "L_DEF_ankle") and not cmds.objExists("L_leg_kinematics"):

            # FK LEG
            fk_leg_instance = fk_leg_module.FKLeg(prefix="L")
            fk_leg_instance.create_fk_leg_joints()
            fk_leg_instance.create_fk_leg_controls()

            # IK LEG
            fk_leg_instance = ik_leg_module.IKLeg(prefix="L")
            fk_leg_instance.create_ik_leg_joints()
            fk_leg_instance.create_ik_leg_controls()
            fk_leg_instance.create_knee_space_swap()

            # # SWITCH LEG
            # switch_leg_instance = switch_leg_module.SwitchLeg(prefix="L")
            # switch_leg_instance.create_ik_fk_switch_leg_controls()
            #
            # # STRETCH LEG
            # if is_stretch_limb:
            #     leg_stretch_instance = leg_stretch_module.LegStretch(prefix="L")
            #     leg_stretch_instance.create_leg_stretch_locators()
            #     leg_stretch_instance.create_leg_stretch_joints()
            #     leg_stretch_instance.create_leg_stretch_nodes()
            #     leg_stretch_instance.create_leg_stretch_nodes()

        if cmds.objExists("R_DEF_upperleg") and cmds.objExists("R_DEF_lowerleg") and cmds.objExists(
                "R_DEF_ankle") and not cmds.objExists("R_leg_kinematics"):

            # FK LEG
            fk_leg_instance = fk_leg_module.FKLeg(prefix="R")
            fk_leg_instance.create_fk_leg_joints()
            fk_leg_instance.create_fk_leg_controls()

            # IK LEG
            fk_leg_instance = ik_leg_module.IKLeg(prefix="R")
            fk_leg_instance.create_ik_leg_joints()
            fk_leg_instance.create_ik_leg_controls()
            fk_leg_instance.create_knee_space_swap()

            # # SWITCH LEG
            # switch_leg_instance = switch_leg_module.SwitchLeg(prefix="L")
            # switch_leg_instance.create_ik_fk_switch_leg_controls()
            #
            # # STRETCH LEG
            # if is_stretch_limb:
            #     leg_stretch_instance = leg_stretch_module.LegStretch(prefix="R")
            #     leg_stretch_instance.create_leg_stretch_locators()
            #     leg_stretch_instance.create_leg_stretch_joints()
            #     leg_stretch_instance.create_leg_stretch_nodes()
            #     leg_stretch_instance.create_leg_stretch_nodes()

        if cmds.objExists("DEF_cog") and cmds.objExists("DEF_pelvis") and cmds.objExists(
                "DEF_spine_01") and cmds.objExists("DEF_spine_02") and cmds.objExists(
                "DEF_spine_03") and cmds.objExists("DEF_neck") and not cmds.objExists("spine_group"):

            # FK LEG GROUP
            if not cmds.objExists("spine_controls"):
                cmds.group(empty=True, name="spine_controls")

            cmds.parent("spine_controls", "controls")

            # FK SPINE
            fk_spine_instance = fk_spine_module.FKSpine()
            fk_spine_instance.create_fk_spine_controls()

            # IK SPINE
            ik_spine_instance = ik_spine_module.IKSpine()
            ik_spine_instance.create_ik_spine_controls()

            # SWITCH SPINE
            switch_spine_instance = switch_spine_module.SwitchSpine()
            switch_spine_instance.create_ik_fk_switch_spine_controls()

            # ROLL SPINE
            if is_roll_limb:
                switch_spine_instance = spine_roll_module.SpineRoll()
                switch_spine_instance.create_spine_roll_nodes()

            # STRETCH SPINE
            if is_stretch_limb:
                spine_stretch_instance = spine_stretch_module.SpineStretch()
                spine_stretch_instance.create_spine_stretch_attributes()
                spine_stretch_instance.create_spine_stretch_nodes()


if __name__ == "__main__":
    main_window = MainWindow()
