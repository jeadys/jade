import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QGroupBox, QPushButton, QTabWidget, QVBoxLayout, QWidget

from ui.actions.connect_module import parent_module_to_selected_module
from ui.widgets.combobox import create_combobox, update_driven_combobox
from ui.widgets.slider import create_spinbox_slider
from ui.widgets.checkbox import create_checkbox
from ui.widgets.container import Container
from ui.widgets.set_attribute import set_attribute
from ui.widgets.tree_widget import tree_widget, TreeWidget


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


class ParentSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.node_widget, self.node_combobox = create_combobox(name="Parent Node", items=["master"])
        self.segment_widget, self.segment_combobox = create_combobox(name="Parent Joint", items=[])
        self.connect_button = QPushButton("connect module")

    def setup_parent_ui(self, layout) -> None:
        layout.addWidget(self.node_widget)
        layout.addWidget(self.segment_widget)
        layout.addWidget(self.connect_button)

        self.connect_button.clicked.connect(parent_module_to_selected_module)

        self.node_combobox.currentIndexChanged.connect(
            lambda: update_driven_combobox(driver_combobox=self.node_combobox, driven_combobox=self.segment_combobox,
                                           attribute="segments"))

    def update_parent_ui(self, module) -> None:
        parent_node = cmds.listConnections(f"{module}.parent_node")
        parent_joint = cmds.listConnections(f"{module}.parent_joint")

        self.node_combobox.setCurrentText(parent_node[0] if parent_node else "")
        self.segment_combobox.setCurrentText(parent_joint[0] if parent_joint else "")


class RelationSettingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.parent_setting: ParentSetting = ParentSetting()
        self.setup_relation_ui()

    def setup_relation_ui(self) -> None:
        self.parent_setting.setup_parent_ui(layout=self.layout)

    def update_relation_ui(self, module) -> None:
        self.parent_setting.update_parent_ui(module=module)


class SettingGroup(QGroupBox):
    def __init__(self):
        super().__init__("Module settings")
        self.setMinimumWidth(300)
        self.settings_layout = QVBoxLayout()
        self.setLayout(self.settings_layout)


settings_group = SettingGroup()
settings_tab_widget = QTabWidget()
settings_group.settings_layout.addWidget(settings_tab_widget)

relation_setting_tab = RelationSettingTab()
mechanism_setting_tab = MechanismSettingTab()

settings_tab_widget.addTab(relation_setting_tab, "Relations")
settings_tab_widget.addTab(mechanism_setting_tab, "Mechanisms")


def update_settings_on_selection(tree: TreeWidget):
    selected_items = tree.selectedItems()
    if not selected_items:
        return

    selected_module = selected_items[0].text(0)
    if not cmds.objExists(selected_module):
        return

    cmds.select(selected_module)

    mechanism_setting_tab.update_mechanism_ui(module=selected_module)
    relation_setting_tab.update_relation_ui(module=selected_module)


tree_widget.itemSelectionChanged.connect(lambda: update_settings_on_selection(tree_widget))

# def update_twist_controls(module):
#     if not cmds.attributeQuery("twist", node=module, exists=True):
#         return
#     twist = cmds.getAttr(f"{module}.twist_enabled")
#     twist_joints = cmds.getAttr(f"{module}.twist_joints")
#     twist_checkbox.setChecked(twist)
#     twist_amount_slider.setValue(twist_joints)
#
#
# def update_stretch_controls(module):
#     if not cmds.attributeQuery("stretch", node=module, exists=True):
#         return
#
#     stretch = cmds.getAttr(f"{module}.stretch_enabled")
#     stretch_checkbox.setChecked(stretch)
#
#
# def update_ribbon_controls(module):
#     if not cmds.attributeQuery("ribbon", node=module, exists=True):
#         return
#
#     ribbon = cmds.getAttr(f"{module}.ribbon_enabled")
#     ribbon_divisions = cmds.getAttr(f"{module}.ribbon_divisions")
#     ribbon_tweaks = cmds.getAttr(f"{module}.tweak_controls")
#     ribbon_checkbox.setChecked(ribbon)
#     ribbon_divisions_slider.setValue(ribbon_divisions)
#     ribbon_tweaks_slider.setValue(ribbon_tweaks)
#
#
# def update_parent_controls(module):
#     parent_node = cmds.listConnections(f"{module}.parent_node")
#     parent_joint = cmds.listConnections(f"{module}.parent_joint")
#
#     node_combobox.setCurrentText(parent_node[0] if parent_node else "")
#     segment_combobox.setCurrentText(parent_joint[0] if parent_joint else "")
