import maya.cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets

from source.get_source import get_source
from ui.actions.refresh_ui import refresh_ui
from ui.widgets.combobox import node_combobox, segment_combobox
from ui.widgets.context_menu import ContextMenu


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, text, font_size, icon):
        super(TreeWidgetItem, self).__init__()
        self.setText(0, text)
        self.setFont(0, QtGui.QFont("Open Sans", font_size))
        self.setIcon(0, QtGui.QIcon(get_source(icon=icon)))


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self):
        super(TreeWidget, self).__init__()
        self.setHeaderHidden(True)
        self.setSortingEnabled(False)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.context_menu = ContextMenu(self)
        self.customContextMenuRequested.connect(self.context_menu.show)

    def add_item(self, item: TreeWidgetItem, parent=None):
        if parent:
            found_parent = self.find_item(parent)
            if found_parent:
                found_parent.addChild(item)
                self.expandItem(found_parent)
                self.setCurrentItem(item)
                return

        self.addTopLevelItem(item)
        self.setCurrentItem(item)

    def remove_item(self, item: TreeWidgetItem):
        current_parent = item.parent()
        if current_parent:
            index = current_parent.indexOfChild(item)
            current_parent.takeChild(index)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)

    def move_item(self, parent):
        selected_items = self.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]

        self.remove_item(item=item)
        self.add_item(item=item, parent=parent)
        refresh_ui(tree=tree_widget, combobox=node_combobox)

    def find_item(self, search: TreeWidgetItem):
        if isinstance(search, QtWidgets.QTreeWidgetItem):
            search_text = search.text(0)
        elif isinstance(search, str):
            search_text = search
        else:
            return None

        items = self.findItems(search_text, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
        if items:
            return items[0]
        return None

    def sort_tree(self):
        current_sort_order = self.header().sortIndicatorOrder()
        new_sort_order = QtCore.Qt.DescendingOrder if current_sort_order == QtCore.Qt.AscendingOrder else QtCore.Qt.AscendingOrder
        self.sortByColumn(0, new_sort_order)


tree_widget = TreeWidget()
refresh_button = QtWidgets.QPushButton("refresh")
refresh_button.clicked.connect(lambda: refresh_ui(tree_widget, node_combobox))


def display_module_parents_in_combobox(tree_widget: TreeWidget):
    selected_items = tree_widget.selectedItems()
    if not selected_items:
        return

    selected_module = selected_items[0].text(0)
    if not cmds.objExists(selected_module):
        return

    cmds.select(selected_module)

    parent_node = cmds.listConnections(f"{selected_module}.parent_node")
    parent_joint = cmds.listConnections(f"{selected_module}.parent_joint")

    node_combobox.setCurrentText(parent_node[0] if parent_node else "")
    segment_combobox.setCurrentText(parent_joint[0] if parent_joint else "")


tree_widget.itemSelectionChanged.connect(lambda: display_module_parents_in_combobox(tree_widget))
