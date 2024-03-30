
from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtWidgets
import maya.cmds as cmds
from importlib import reload
import inspect

# Joints
import joints.arm as arm_module
import joints.leg as leg_module
import joints.spine as spine_module

# Arm
import controllers.arm_fk as arm_fk_module
import controllers.arm_ik as arm_ik_module
import controllers.arm_switch as arm_switch_module
import mechanisms.arm_stretch as arm_stretch_module
import mechanisms.arm_twist as arm_twist_module

# Leg
import controllers.leg_fk as leg_fk_module
import controllers.leg_ik as leg_ik_module
import controllers.leg_switch as leg_switch_module
import mechanisms.leg_stretch as leg_stretch_module
import mechanisms.leg_twist as leg_twist_module

# Spine
import controllers.spine_fk as spine_fk_module
import controllers.spine_ik as spine_ik_module
import controllers.spine_switch as spine_switch_module
import mechanisms.spine_roll as spine_roll_module
import mechanisms.spine_stretch as spine_stretch_module

import utilities.snap_fk_to_ik as snap_fk_to_ik_module
import utilities.snap_ik_to_fk as snap_ik_to_fk_module

import mechanisms.foot_roll as foot_roll_module

import windows.arm_window as arm_window_module
import windows.leg_window as leg_window_module
import os

from ui.widgets.checkbox import create_checkbox
from ui.widgets.combobox import create_combobox
from ui.widgets.line_edit import create_line_edit
from ui.widgets.slider import create_slider
from ui.widgets.spinbox import create_spinbox

reload(arm_window_module)
reload(leg_window_module)

reload(arm_module)
reload(arm_fk_module)
reload(arm_ik_module)
reload(arm_switch_module)
reload(arm_stretch_module)
reload(arm_twist_module)

reload(leg_module)
reload(leg_fk_module)
reload(leg_ik_module)
reload(leg_switch_module)
reload(leg_stretch_module)
reload(leg_twist_module)

reload(spine_module)
reload(spine_fk_module)
reload(spine_ik_module)
reload(spine_switch_module)
reload(spine_roll_module)
reload(spine_stretch_module)

reload(snap_fk_to_ik_module)
reload(snap_ik_to_fk_module)

reload(foot_roll_module)


def undoable(func):
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            result = func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
        return result
    return wrapper


class MayaUITemplate(QtWidgets.QWidget):
    window = None

    def __init__(self, parent=None):
        super(MayaUITemplate, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setFixedSize(250, 250)

        script_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
        icon_path = os.path.join(script_dir, "src", "icons")

        main_layout = QtWidgets.QVBoxLayout(self)

        module_group = QtWidgets.QGroupBox("modules")
        module_layout = QtWidgets.QVBoxLayout()
        module_group.setLayout(module_layout)
        main_layout.addWidget(module_group)

        limb_modules = ["arm", "leg", "spine"]
        limb_module_widget, self.limb_module_combobox = create_combobox(name="limb", items=limb_modules)
        self.limb_module_combobox.currentTextChanged.connect(self.limb_changed)
        module_layout.addWidget(limb_module_widget)

        limb_sides = ["L", "R"]
        self.limb_side_widget, self.limb_side_combobox = create_combobox(name="side", items=limb_sides)
        module_layout.addWidget(self.limb_side_widget)

        self.spine_count_widget, self.spine_count_slider = create_slider(name="spine count", value=5, minimum=5,
                                                                         maximum=10)
        self.spine_count_widget.setVisible(False)
        module_layout.addWidget(self.spine_count_widget)

        orientation_group = QtWidgets.QGroupBox("orientations")
        orientation_layout = QtWidgets.QVBoxLayout()
        orientation_group.setLayout(orientation_layout)
        main_layout.addWidget(orientation_group)

        rotation_orders = ["xyz", "yzx", "zxy", "zyx", "yxz", "xzy"]
        rotation_order_widget, self.rotation_order_combobox = create_combobox(name="rotation order",
                                                                              items=rotation_orders)
        orientation_layout.addWidget(rotation_order_widget)

        joint_orientations = ["yzx - zup", "yzx - zdown"]
        joint_orientation_widget, self.joint_orientation_combobox = create_combobox(name="joint orientation",
                                                                                    items=joint_orientations)
        orientation_layout.addWidget(joint_orientation_widget)

        mechanism_group = QtWidgets.QGroupBox("mechanisms")
        mechanism_layout = QtWidgets.QVBoxLayout()
        mechanism_group.setLayout(mechanism_layout)
        main_layout.addWidget(mechanism_group)

        twist_widget, self.twist_checkbox = create_checkbox(name="twist", is_checked=True)
        mechanism_layout.addWidget(twist_widget)

        stretch_widget, self.stretch_checkbox = create_checkbox(name="stretch", is_checked=True)
        mechanism_layout.addWidget(stretch_widget)

        operation_group = QtWidgets.QGroupBox("operations")
        operation_layout = QtWidgets.QVBoxLayout()
        operation_group.setLayout(operation_layout)
        main_layout.addWidget(operation_group)

        locator_button = QtWidgets.QPushButton("create locators")
        locator_button.clicked.connect(self.create_locators)
        operation_layout.addWidget(locator_button)

        joint_button = QtWidgets.QPushButton("create joints")
        joint_button.clicked.connect(self.create_joints)
        operation_layout.addWidget(joint_button)

    def radio_selected(self):
        sender = self.sender()
        if sender.isChecked():
            print("Selected option:", sender.text())

    def select_module(self, index):
        self.selected_module = self.select_module_combo.itemText(index)

    def select_side(self, index):
        self.selected_side = self.select_side_combo.itemText(index)

    @undoable
    def create_locators(self):
        match self.selected_module:
            case "arm":
                arm_instance = arm_module.Arm(prefix=self.selected_side)
                arm_instance.create_arm_locators()
            case "leg":
                leg_instance = leg_module.Leg(prefix=self.selected_side)
                leg_instance.create_leg_locators()
            case "spine":
                spine_instance = spine_module.Spine(prefix="C", spine_count=self.slider.value())
                spine_instance.create_spine_locators()
        cmds.select(deselect=True)

    @undoable
    def create_joints(self):
        match self.selected_module:
            case "arm":
                arm_instance = arm_module.Arm(prefix=self.selected_side)
                arm_instance.create_arm_joints()
            case "leg":
                leg_instance = leg_module.Leg(prefix=self.selected_side)
                leg_instance.create_leg_joints()
            case "spine":
                spine_instance = spine_module.Spine(prefix="C", spine_count=self.slider.value())
                spine_instance.create_spine_joints()
        cmds.select(deselect=True)

    @undoable
    def create_controls(self, *_args):
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

        match self.selected_module:
            case "arm":
                # FK ARM
                fk_arm_instance = arm_fk_module.ArmFK(prefix=self.selected_side)
                fk_arm_instance.create_arm_fk()

                # IK ARM
                ik_arm_instance = arm_ik_module.ArmIK(prefix=self.selected_side)
                ik_arm_instance.create_arm_ik()

                # SWITCH ARM
                arm_switch_instance = arm_switch_module.ArmSwitch(prefix=self.selected_side)
                arm_switch_instance.create_arm_switch()

                # TWIST ARM
                if self.add_twist:
                    arm_twist_instance = arm_twist_module.ArmTwist(prefix=self.selected_side)
                    arm_twist_instance.create_arm_twist()

                # STRETCH ARM
                if self.add_stretch:
                    arm_stretch_instance = arm_stretch_module.ArmStretch(prefix=self.selected_side)
                    arm_stretch_instance.create_arm_stretch()

            case "leg":
                # FK LEG
                leg_fk_instance = leg_fk_module.LegFK(prefix=self.selected_side)
                leg_fk_instance.create_leg_fk()

                # IK LEG
                leg_ik_instance = leg_ik_module.LegIK(prefix=self.selected_side)
                leg_ik_instance.create_leg_ik()

                # SWITCH LEG
                leg_switch_instance = leg_switch_module.LegSwitch(prefix=self.selected_side)
                leg_switch_instance.create_leg_switch()

                # TWIST LEG
                if self.add_twist:
                    leg_twist_instance = leg_twist_module.LegTwist(prefix=self.selected_side)
                    leg_twist_instance.create_leg_twist()

                # STRETCH LEG
                if self.add_stretch:
                    leg_stretch_instance = leg_stretch_module.LegStretch(prefix=self.selected_side)
                    leg_stretch_instance.create_leg_stretch()

            case "spine":
                # IK SPINE
                ik_spine_instance = spine_ik_module.IKSpine(prefix="C", spine_count=self.slider.value())
                ik_spine_instance.create_ik_spine()


def open_window():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if 'auto_rig' in win.objectName():
                win.destroy()

    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    MayaUITemplate.window = MayaUITemplate(parent=maya_main_window)
    MayaUITemplate.window.setObjectName('auto_rig')
    MayaUITemplate.window.setWindowTitle('Maya UI Template')
    MayaUITemplate.window.show()


if __name__ == "__main__":
    open_window()
