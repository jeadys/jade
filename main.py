import maya.cmds as cmds
from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtCore, QtWidgets

from ui.widgets.checkbox import create_checkbox
from ui.widgets.combobox import create_combobox
from ui.widgets.slider import create_slider

from segments.arm import Arm
from segments.leg import Leg
from segments.spine import Spine
from segments.finger import Finger
from segments.front_leg import FrontLeg
from segments.rear_leg import RearLeg
from segments.quadrupled_spine import QuadrupledSpine

from utilities.unload_packages import unload_packages


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
        self.resize(450, 350)

        main_layout = QtWidgets.QVBoxLayout(self)

        module_group = QtWidgets.QGroupBox("modules")
        module_layout = QtWidgets.QVBoxLayout()
        module_group.setLayout(module_layout)
        main_layout.addWidget(module_group)

        limb_modules: list[str] = ["arm", "leg", "spine", "front_leg", "rear_leg", "quadrupled_spine"]
        limb_module_widget, self.limb_module_combobox = create_combobox(name="limb", items=limb_modules)
        self.limb_module_combobox.currentTextChanged.connect(self.limb_changed)
        module_layout.addWidget(limb_module_widget)

        limb_sides: list[str] = ["L", "R"]
        self.limb_side_widget, self.limb_side_combobox = create_combobox(name="side", items=limb_sides)
        module_layout.addWidget(self.limb_side_widget)

        self.finger_count_widget, self.finger_count_slider = create_slider(name="finger count", value=5, minimum=1,
                                                                           maximum=5)
        module_layout.addWidget(self.finger_count_widget)

        self.spine_count_widget, self.spine_count_slider = create_slider(name="spine count", value=5, minimum=5,
                                                                         maximum=10)
        self.spine_count_widget.setVisible(False)
        module_layout.addWidget(self.spine_count_widget)

        orientation_group = QtWidgets.QGroupBox("orientations")
        orientation_layout = QtWidgets.QVBoxLayout()
        orientation_group.setLayout(orientation_layout)
        main_layout.addWidget(orientation_group)

        rotation_orders: list[str] = ["XYZ", "YZX", "ZXY", "ZYX", "YXZ", "XZY"]
        rotation_order_widget, self.rotation_order_combobox = create_combobox(name="rotation order",
                                                                              items=rotation_orders)
        orientation_layout.addWidget(rotation_order_widget)

        joint_orientations: list[str] = ["yzx - zup"]
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

        control_button = QtWidgets.QPushButton("create controls")
        control_button.clicked.connect(self.create_controls)
        operation_layout.addWidget(control_button)

    def limb_changed(self):
        if self.limb_module_combobox.currentText() == "arm":
            self.finger_count_widget.setVisible(True)
            self.limb_side_widget.setVisible(True)
            self.spine_count_widget.setVisible(False)
        elif self.limb_module_combobox.currentText() == "spine":
            self.spine_count_widget.setVisible(True)
            self.limb_side_widget.setVisible(False)
            self.finger_count_widget.setVisible(False)
        else:
            self.spine_count_widget.setVisible(False)
            self.limb_side_widget.setVisible(True)
            self.finger_count_widget.setVisible(False)

    @undoable
    def create_locators(self):
        prefix = self.limb_side_combobox.currentText()
        match self.limb_module_combobox.currentText():
            case "arm":
                arm_instance = Arm(prefix=prefix)
                arm_locators = arm_instance.create_arm_locators()

                for index in range(self.finger_count_slider.value()):
                    finger_instance = Finger(prefix=prefix, current=index)
                    finger_locators = finger_instance.create_finger_locators()

                    cmds.parent(finger_locators[0], arm_locators[-1])
            case "leg":
                leg_instance = Leg(prefix=prefix)
                leg_instance.create_leg_locators()
            case "spine":
                spine_instance = Spine(spine_count=self.spine_count_slider.value())
                spine_instance.create_spine_locators()
            case "front_leg":
                front_leg_instance = FrontLeg(prefix=prefix)
                front_leg_instance.create_leg_locators()
            case "rear_leg":
                rear_leg_instance = RearLeg(prefix=prefix)
                rear_leg_instance.create_leg_locators()
            case "quadrupled_spine":
                quadrupled_spine_instance = QuadrupledSpine(prefix="C", spine_count=self.spine_count_slider.value())
                quadrupled_spine_instance.create_spine_locators()

        cmds.select(deselect=True)

    @undoable
    def create_joints(self):
        rotation_order = self.rotation_order_combobox.currentText()
        joint_orientation = self.joint_orientation_combobox.currentText()
        prefix = self.limb_side_combobox.currentText()

        match self.limb_module_combobox.currentText():
            case "arm":
                arm_instance = Arm(prefix=prefix)
                arm_joints = arm_instance.create_arm_joints(rotation_order=rotation_order,
                                                            joint_orientation=joint_orientation)

                for index in range(self.finger_count_slider.value()):
                    finger_instance = Finger(prefix=prefix, current=index)
                    finger_joints = finger_instance.create_finger_joints(rotation_order=rotation_order,
                                                                         joint_orientation=joint_orientation)

                    cmds.parent(finger_joints[0], arm_joints[-1])
            case "leg":
                leg_instance = Leg(prefix=prefix)
                leg_instance.create_leg_joints(rotation_order=rotation_order, joint_orientation=joint_orientation)
            case "spine":
                spine_instance = Spine(spine_count=self.spine_count_slider.value())
                spine_instance.create_spine_joints(rotation_order=rotation_order, joint_orientation=joint_orientation)
            case "front_leg":
                front_leg_instance = FrontLeg(prefix=prefix)
                front_leg_instance.create_leg_joints(rotation_order=rotation_order, joint_orientation=joint_orientation)
            case "rear_leg":
                rear_leg_instance = RearLeg(prefix=prefix)
                rear_leg_instance.create_leg_joints(rotation_order=rotation_order, joint_orientation=joint_orientation)
            case "quadrupled_spine":
                quadrupled_spine_instance = QuadrupledSpine(prefix="C", spine_count=self.spine_count_slider.value())
                quadrupled_spine_instance.create_spine_joints(rotation_order=rotation_order,
                                                              joint_orientation=joint_orientation)

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

        prefix = self.limb_side_combobox.currentText()
        rotation_order = self.rotation_order_combobox.currentText()
        match self.limb_module_combobox.currentText():
            case "arm":
                arm_instance = Arm(prefix=prefix)
                arm_instance.create_arm_controls(rotation_order=rotation_order)

                for index in range(self.finger_count_slider.value()):
                    finger_instance = Finger(prefix=prefix, current=index)
                    finger_instance.create_finger_controls(rotation_order=rotation_order)
            case "leg":
                leg_instance = Leg(prefix=prefix)
                leg_instance.create_leg_controls(rotation_order=rotation_order)
            case "spine":
                spine_instance = Spine(prefix="C", spine_count=self.spine_count_slider.value())
                spine_instance.create_spine_controls(rotation_order=rotation_order)
            case "front_leg":
                front_leg_instance = FrontLeg(prefix=prefix)
                front_leg_instance.create_leg_controls(rotation_order=rotation_order)
            case "rear_leg":
                rear_leg_instance = RearLeg(prefix=prefix)
                rear_leg_instance.create_leg_controls(rotation_order=rotation_order)
            case "quadrupled_spine":
                quadrupled_spine_instance = QuadrupledSpine(prefix="C", spine_count=self.spine_count_slider.value())
                quadrupled_spine_instance.create_spine_controls(rotation_order=rotation_order)


def open_window():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if 'auto_rig' in win.objectName():
                win.destroy()

    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    MayaUITemplate.window = MayaUITemplate(parent=maya_main_window)
    MayaUITemplate.window.setObjectName('auto_rig')
    MayaUITemplate.window.setWindowTitle('Maya Auto Rig')
    MayaUITemplate.window.show()


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        unload_packages(silent=False, packages=["segments", "kinematics", "mechanisms", "utilities", "ui"])
    open_window()
