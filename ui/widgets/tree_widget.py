from maya import cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets

from ui.actions.clone_module import clone_module, remove_module
from ui.icons.get_source import get_source
from ui.settings.relation_setting import parent_setting


class TreeContextMenu:
    def __init__(self, tree):
        self.tree = tree

    def show(self, position):
        item = self.tree.itemAt(position)
        if item:
            self.item_context_menu(item, position)
        else:
            self.tree_context_menu(position)

    def item_context_menu(self, item, position):
        menu = QtWidgets.QMenu()
        clone_action = menu.addAction("Clone")
        remove_action = menu.addAction("Remove")

        action = menu.exec_(self.tree.mapToGlobal(position))

        if action == remove_action:
            remove_module(item)
            refresh_ui()
        elif action == clone_action:
            clone_module(item, original_prefix="L_", clone_prefix="R_")
            refresh_ui()

    def tree_context_menu(self, position):
        menu = QtWidgets.QMenu()
        refresh_action = menu.addAction("Refresh")

        action = menu.exec_(self.tree.mapToGlobal(position))

        if action == refresh_action:
            refresh_ui()


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
        self.context_menu = TreeContextMenu(self)
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
refresh_button.clicked.connect(lambda: refresh_ui())


def refresh_ui():
    tree_widget.clear()
    parent_setting.parent_node_combobox.clear()
    parent_setting.parent_node_combobox.addItem("master")
    refresh_modules("master")


def refresh_modules(module):
    if not cmds.objExists(module):
        return

    children = cmds.listConnections(f"{module}.children") or []
    for child in children:
        populate_tree(child)
        populate_combobox(child)
        refresh_modules(child)


def populate_tree(child):
    root_item = QtWidgets.QTreeWidgetItem()
    root_item.setText(0, child)
    root_item.setFont(0, QtGui.QFont("Open Sans", 10))
    root_item.setIcon(0, QtGui.QIcon(get_source(icon=cmds.getAttr(f"{child}.module_type"))))

    parent_node = cmds.listConnections(f"{child}.parent_node") or None
    tree_widget.add_item(item=root_item, parent=parent_node[0] if parent_node else None)


def populate_combobox(child):
    icon = QtGui.QIcon(get_source(icon=cmds.getAttr(f"{child}.module_type")))
    parent_setting.parent_node_combobox.addItem(icon, child)
