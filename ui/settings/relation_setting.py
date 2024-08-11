import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton, QVBoxLayout, QWidget

# from ui.actions.connect_module import parent_module_to_selected_module
from ui.widgets.combobox import create_combobox, update_driven_combobox


class ParentSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.parent_node_widget, self.parent_node_combobox = create_combobox(name="Parent Node", items=["master"])
        self.parent_joint_widget, self.parent_joint_combobox = create_combobox(name="Parent Joint", items=[])
        self.connect_parent_button = QPushButton("connect module")

    def setup_parent_ui(self, layout) -> None:
        layout.addWidget(self.parent_node_widget)
        layout.addWidget(self.parent_joint_widget)
        layout.addWidget(self.connect_parent_button)

        # self.connect_parent_button.clicked.connect(parent_module_to_selected_module)

        self.parent_node_combobox.currentIndexChanged.connect(
            lambda: update_driven_combobox(driver_combobox=self.parent_node_combobox,
                                           driven_combobox=self.parent_joint_combobox,
                                           attribute="segments"))

    def update_parent_ui(self, module) -> None:
        parent_node = cmds.listConnections(f"{module}.parent_node")
        parent_joint = cmds.listConnections(f"{module}.parent_joint")

        self.parent_node_combobox.setCurrentText(parent_node[0] if parent_node else "")
        self.parent_joint_combobox.setCurrentText(parent_joint[0] if parent_joint else "")


class RelationSettingTab(QWidget):
    def __init__(self, test: ParentSetting):
        super().__init__()
        self.test = test

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.setup_relation_ui()

    def setup_relation_ui(self) -> None:
        self.test.setup_parent_ui(layout=self.layout)

    def update_relation_ui(self, module) -> None:
        self.test.update_parent_ui(module=module)


parent_setting = ParentSetting()
relation_setting_tab = RelationSettingTab(test=parent_setting)
