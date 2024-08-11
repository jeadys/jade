import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QVBoxLayout, QWidget

from ui.widgets.slider import create_spinbox_slider
from ui.widgets.checkbox import create_checkbox
from ui.widgets.container import Container
from ui.widgets.set_attribute import set_attribute


class MechanismSettingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.twist_setting: TwistSetting = TwistSetting()
        self.stretch_setting: StretchSetting = StretchSetting()
        self.ribbon_setting: RibbonSetting = RibbonSetting()

        self.setup_mechanism_ui()

    def setup_mechanism_ui(self) -> None:
        self.twist_setting.setup_twist_ui(layout=self.layout)
        self.stretch_setting.setup_stretch_ui(layout=self.layout)
        self.ribbon_setting.setup_ribbon_ui(layout=self.layout)

    def update_mechanism_ui(self, module) -> None:
        self.twist_setting.update_twist_ui(module=module)
        self.stretch_setting.update_stretch_ui(module=module)
        self.ribbon_setting.update_ribbon_ui(module=module)


class TwistSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.twist_toggle_widget, self.twist_toggle_checkbox = create_checkbox(name="add twist", is_checked=True)
        self.twist_joints_widget, self.twist_joints_spinbox, self.twist_joints_slider = create_spinbox_slider(
            name="joint", value=1, minimum=1, maximum=5)

    def setup_twist_ui(self, layout) -> None:
        twist_container = Container("Twist")
        layout.addWidget(twist_container)

        twist_content = QGridLayout(twist_container.contentWidget)

        self.twist_toggle_checkbox.stateChanged.connect(
            lambda: set_attribute("twist_enabled", self.twist_toggle_checkbox.isChecked()))

        self.twist_joints_slider.sliderReleased.connect(
            lambda: set_attribute(attribute="twist_joints", value=self.twist_joints_slider.value()))
        self.twist_joints_spinbox.editingFinished.connect(
            lambda: set_attribute(attribute="twist_joints", value=self.twist_joints_slider.value()))

        twist_content.addWidget(self.twist_toggle_widget)
        twist_content.addWidget(self.twist_joints_widget)

    def update_twist_ui(self, module) -> None:
        twist_toggle = cmds.getAttr(f"{module}.twist_enabled")
        twist_joints = cmds.getAttr(f"{module}.twist_joints")

        self.twist_toggle_checkbox.setChecked(twist_toggle)
        self.twist_joints_slider.setValue(twist_joints)


class StretchSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.stretch_toggle_widget, self.stretch_toggle_checkbox = create_checkbox(name="add stretch", is_checked=True)

    def setup_stretch_ui(self, layout) -> None:
        stretch_container = Container("Stretch")
        layout.addWidget(stretch_container)

        stretch_content = QGridLayout(stretch_container.contentWidget)

        self.stretch_toggle_checkbox.stateChanged.connect(
            lambda: set_attribute("stretch_enabled", self.stretch_toggle_checkbox.isChecked()))

        stretch_content.addWidget(self.stretch_toggle_widget)

    def update_stretch_ui(self, module) -> None:
        stretch_toggle = cmds.getAttr(f"{module}.ribbon_enabled")
        self.stretch_toggle_checkbox.setChecked(stretch_toggle)


class RibbonSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.ribbon_toggle_widget, self.ribbon_toggle_checkbox = create_checkbox(name="add ribbon", is_checked=True)
        self.ribbon_divisions_widget, self.ribbon_divisions_spinbox, self.ribbon_divisions_slider = create_spinbox_slider(
            name="divisions", value=1, minimum=1, maximum=20)
        self.ribbon_tweaks_widget, self.ribbon_tweaks_spinbox, self.ribbon_tweaks_slider = create_spinbox_slider(
            name="tweaks", value=1, minimum=1, maximum=5)

    def setup_ribbon_ui(self, layout) -> None:
        ribbon_container = Container("Ribbon")
        layout.addWidget(ribbon_container)

        ribbon_content = QGridLayout(ribbon_container.contentWidget)

        self.ribbon_toggle_checkbox.stateChanged.connect(
            lambda: set_attribute("ribbon_enabled", self.ribbon_toggle_checkbox.isChecked()))

        self.ribbon_divisions_slider.sliderReleased.connect(
            lambda: set_attribute(attribute="ribbon_divisions", value=self.ribbon_divisions_slider.value()))
        self.ribbon_divisions_spinbox.editingFinished.connect(
            lambda: set_attribute(attribute="ribbon_divisions", value=self.ribbon_divisions_slider.value()))

        self.ribbon_tweaks_slider.sliderReleased.connect(
            lambda: set_attribute(attribute="tweak_controls", value=self.ribbon_tweaks_slider.value()))
        self.ribbon_tweaks_spinbox.editingFinished.connect(
            lambda: set_attribute(attribute="tweak_controls", value=self.ribbon_tweaks_slider.value()))

        ribbon_content.addWidget(self.ribbon_toggle_widget)
        ribbon_content.addWidget(self.ribbon_divisions_widget)
        ribbon_content.addWidget(self.ribbon_tweaks_widget)

    def update_ribbon_ui(self, module) -> None:
        ribbon_toggle = cmds.getAttr(f"{module}.ribbon_enabled")
        ribbon_divisions = cmds.getAttr(f"{module}.ribbon_divisions")
        ribbon_tweaks = cmds.getAttr(f"{module}.tweak_controls")

        self.ribbon_toggle_checkbox.setChecked(ribbon_toggle)
        self.ribbon_divisions_slider.setValue(ribbon_divisions)
        self.ribbon_tweaks_slider.setValue(ribbon_tweaks)


mechanism_setting_tab = MechanismSettingTab()
