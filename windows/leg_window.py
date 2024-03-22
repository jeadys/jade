import maya.cmds as cmds
from importlib import reload

import joints.leg as leg_module
import controllers.leg_fk as leg_fk_module
import controllers.leg_ik as leg_ik_module
import controllers.leg_switch as leg_switch_module
import mechanisms.leg_stretch as leg_stretch_module
import mechanisms.leg_twist as leg_twist_module

reload(leg_module)
reload(leg_fk_module)
reload(leg_ik_module)
reload(leg_switch_module)
reload(leg_stretch_module)
reload(leg_twist_module)


class LegWindow:

    def __init__(self):
        self.leg_window = None
        self.window_name = "LegWindow"
        self.prefix = "L"
        self.stretch = True
        self.twist = True

        # Check if the window already exists and close it
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)
        if cmds.window("ArmWindow", exists=True):
            cmds.deleteUI("ArmWindow", window=True)

        self.create_leg_window()

    def create_leg_window(self):
        self.leg_window = cmds.window(self.window_name, title=self.window_name, widthHeight=(300, 300), sizeable=False)
        main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=20, margins=10)

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=(1, 2))
        cmds.text("Add stretch")
        radio = cmds.radioButtonGrp("Side", columnWidth2=[50, 50], numberOfRadioButtons=2, labelArray2=['Left', 'Right'], select=1, onCommand=self.change_side)
        cmds.setParent(main_layout)

        cmds.button(label="Add Locators", height=30, command=self.create_leg_locator_button)
        cmds.button(label="Add Joints", height=30, command=self.create_leg_joint_button)
        cmds.button(label="Add Controls", height=30, command=self.create_leg_rig_button)
        cmds.setParent(main_layout)

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=(1, 2))
        cmds.text("Add stretch")
        cmds.radioButtonGrp("add_stretch", columnWidth2=[50, 50], numberOfRadioButtons=2, labelArray2=['Yes', 'No'], select=self.stretch, onCommand=self.add_stretch_value)
        cmds.setParent(main_layout)

        cmds.rowLayout(numberOfColumns=2, adjustableColumn=(1, 2))
        cmds.text("Add twist")
        cmds.radioButtonGrp("add_twist", columnWidth2=[50, 50], numberOfRadioButtons=2, labelArray2=['Yes', 'No'], select=self.twist, onCommand=self.add_twist_value)
        cmds.setParent(main_layout)

        cmds.showWindow(self.leg_window)

    def change_side(self, *_args):
        side = cmds.radioButtonGrp("Side", query=True, select=True)
        self.prefix = "L" if side == 1 else "R"

    def add_stretch_value(self, *_args):
        stretch = cmds.radioButtonGrp("add_stretch", query=True, select=True)
        self.stretch = True if stretch == 1 else False

    def add_twist_value(self, *_args):
        twist = cmds.radioButtonGrp("add_twist", query=True, select=True)
        self.twist = True if twist == 1 else False

    def create_leg_locator_button(self, *_args):
        leg_instance = leg_module.Leg(prefix=self.prefix)
        leg_instance.create_leg_locators()

    def create_leg_joint_button(self, *_args):
        is_auto_parent = cmds.checkBox("is_auto_parent", query=True, value=True)

        leg_instance = leg_module.Leg(prefix=self.prefix)
        leg_instance.create_leg_joints(is_auto_parent)

    def create_leg_rig_button(self, *_args):
        self.create_groups()
        # FK ARM
        fk_leg_instance = leg_fk_module.LegFK(prefix=self.prefix)
        fk_leg_instance.create_leg_fk()

        # IK ARM
        ik_leg_instance = leg_ik_module.LegIK(prefix=self.prefix)
        ik_leg_instance.create_leg_ik()

        # SWITCH ARM
        leg_switch_instance = leg_switch_module.LegSwitch(prefix=self.prefix)
        leg_switch_instance.create_leg_switch()

        # TWIST ARM
        if self.twist:
            leg_twist_instance = leg_twist_module.LegTwist(prefix=self.prefix)
            leg_twist_instance.create_leg_twist()

        # STRETCH ARM
        if self.stretch:
            leg_stretch_instance = leg_stretch_module.LegStretch(prefix=self.prefix)
            leg_stretch_instance.create_leg_stretch()

    @staticmethod
    def create_groups():
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
