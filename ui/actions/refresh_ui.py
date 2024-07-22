import maya.cmds as cmds
from PySide2 import QtGui, QtWidgets

from source.get_source import get_source


def refresh_ui(tree: QtWidgets.QTreeWidget, combobox: QtWidgets.QComboBox):
    tree.clear()
    combobox.clear()
    combobox.addItem("master")
    refresh_modules("master", tree, combobox)


def refresh_modules(module, tree: QtWidgets.QTreeWidget, combobox: QtWidgets.QComboBox):
    if not cmds.objExists(module):
        return

    children = cmds.listConnections(f"{module}.children") or []
    for child in children:
        populate_tree(child, tree)
        populate_combobox(child, combobox)
        refresh_modules(child, tree, combobox)


def populate_tree(child, tree: QtWidgets.QTreeWidget):
    root_item = QtWidgets.QTreeWidgetItem()
    root_item.setText(0, child)
    root_item.setFont(0, QtGui.QFont("Open Sans", 10))
    root_item.setIcon(0, QtGui.QIcon(get_source(icon=cmds.getAttr(f"{child}.module_type"))))

    parent_node = cmds.listConnections(f"{child}.parent_node") or None
    tree.add_item(item=root_item, parent=parent_node[0] if parent_node else None)


def populate_combobox(child, combobox: QtWidgets.QComboBox):
    icon = QtGui.QIcon(get_source(icon=cmds.getAttr(f"{child}.module_type")))
    combobox.addItem(icon, child)
