import maya.cmds as cmds
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QComboBox, QHBoxLayout, QLabel, QWidget

from ui.icons.get_source import get_source


class ComboboxWidget(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)
        self.disabled_index = None

    def disable_item(self, name):
        index = node_combobox.findText(name)
        if not index:
            return

        if self.disabled_index:
            self.view().setRowHidden(self.disabled_index, False)

        self.view().setRowHidden(index, True)
        self.disabled_index = index


def create_combobox(name: str, items: list[str]) -> tuple[QWidget, QComboBox]:
    widget = QWidget()

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    label = QLabel(name)
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    label.setFixedWidth(75)

    combobox = QComboBox()
    combobox.addItems(items)

    layout.addWidget(label)
    layout.addWidget(combobox)

    return widget, combobox


node_widget, node_combobox = create_combobox(name="Parent Node", items=["master"])
segment_widget, segment_combobox = create_combobox(name="Parent Joint", items=[])


def update_driven_combobox(driver_combobox: QComboBox, driven_combobox: QComboBox, attribute: str):
    selected_item = driver_combobox.currentText()
    if not cmds.objExists(selected_item):
        return

    has_attribute = cmds.attributeQuery(attribute, node=selected_item, exists=True)
    items = cmds.listConnections(f"{selected_item}.{attribute}") if has_attribute else []

    driven_combobox.clear()

    for index, item in enumerate(items):
        icon = QIcon(get_source(icon="joint"))
        driven_combobox.addItem(item)
        driven_combobox.setItemIcon(index, icon)
