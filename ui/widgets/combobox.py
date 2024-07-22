import maya.cmds as cmds
from PySide2 import QtGui, QtWidgets

from source.get_source import get_source


def create_combobox(name: str, items: list[str]):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    combobox = QtWidgets.QComboBox()
    layout.addWidget(combobox)
    for item in items:
        combobox.addItem(item)

    return widget, combobox


node_widget, node_combobox = create_combobox(name="Parent Node", items=["master"])
node_combobox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

segment_widget, segment_combobox = create_combobox(name="Parent Joint", items=[])
segment_combobox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


def update_driven_combobox(driver_combobox: QtWidgets.QComboBox, driven_combobox: QtWidgets.QComboBox, attribute: str):
    selected_item = driver_combobox.currentText()
    if not cmds.objExists(selected_item):
        return

    has_attribute = cmds.attributeQuery(attribute, node=selected_item, exists=True)
    items = cmds.listConnections(f"{selected_item}.{attribute}") if has_attribute else []

    driven_combobox.clear()

    for index, item in enumerate(items):
        icon = QtGui.QIcon(get_source(icon="joint"))
        driven_combobox.addItem(item)
        driven_combobox.setItemIcon(index, icon)


node_combobox.currentIndexChanged.connect(
    lambda val: update_driven_combobox(driver_combobox=node_combobox, driven_combobox=segment_combobox,
                                       attribute="segments"))
