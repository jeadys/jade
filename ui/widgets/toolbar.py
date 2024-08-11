from PySide2 import QtWidgets, QtCore, QtGui
from ui.icons.get_source import get_source
from ui.widgets.tree_widget import tree_widget, refresh_ui
from ui.widgets.combobox import node_combobox


class ActionWidget(QtWidgets.QAction):
    def __init__(self, text, icon):
        super().__init__()
        self.setText(text)
        self.setIcon(QtGui.QIcon(get_source(icon=icon)))


class ToolbarWidget(QtWidgets.QToolBar):
    def __init__(self, title="toolbar"):
        super().__init__(title)
        self.setIconSize(QtCore.QSize(24, 24))
        self.actions = []

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(self.spacer)

    def add_action(self, text, icon, callback=None):
        action = ActionWidget(text=text, icon=icon)
        if callback:
            action.triggered.connect(callback)
        self.addAction(action)
        self.actions.append(action)


tree_toolbar = ToolbarWidget()

tree_toolbar.add_action(text="export rig", icon="download")
tree_toolbar.add_action(text="import rig", icon="upload")
tree_toolbar.add_action(text="refresh", icon="refresh", callback=refresh_ui)
