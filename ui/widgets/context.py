from PySide2 import QtWidgets

from ui.actions.clone_module import clone_module, remove_module
from ui.widgets.tree_widget import refresh_ui


class ContextMenu:
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
