import maya.cmds as cmds
from PySide2.QtWidgets import QGroupBox, QTabWidget, QVBoxLayout

from ui.settings.mechanism_setting import mechanism_setting_tab, MechanismSettingTab
from ui.settings.relation_setting import relation_setting_tab, RelationSettingTab
from ui.widgets.tree_widget import tree_widget, TreeWidget


class SettingGroup(QGroupBox):
    def __init__(self, relation_setting: RelationSettingTab, mechanism_setting: MechanismSettingTab):
        super().__init__("Module settings")
        self.setMinimumWidth(300)
        self.settings_layout = QVBoxLayout()
        self.setLayout(self.settings_layout)

        self.settings_tab_widget = QTabWidget()
        self.settings_layout.addWidget(self.settings_tab_widget)

        self.relation_setting = relation_setting
        self.mechanism_setting = mechanism_setting

        self.settings_tab_widget.addTab(self.relation_setting, "Relations")
        self.settings_tab_widget.addTab(self.mechanism_setting, "Mechanisms")

    def update_settings_on_selection(self, tree: TreeWidget):
        selected_items = tree.selectedItems()
        if not selected_items:
            return

        selected_module = selected_items[0].text(0)
        if not cmds.objExists(selected_module):
            return

        cmds.select(selected_module)

        self.relation_setting.update_relation_ui(module=selected_module)
        self.mechanism_setting.update_mechanism_ui(module=selected_module)


setting_group = SettingGroup(relation_setting=relation_setting_tab, mechanism_setting=mechanism_setting_tab)
tree_widget.itemSelectionChanged.connect(lambda: setting_group.update_settings_on_selection(tree_widget))
