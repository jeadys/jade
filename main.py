from maya import OpenMayaUI
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

from data.read_data import import_rig_data
from data.write_data import export_rig_data
from ui.actions.build_rig import build_rig
from ui.actions.tree_view import connect_button, delete_button, node_widget, segment_widget, tree_view
from ui.widgets.tab_widget import tab_widget
from utilities.unload_packages import unload_packages


class MainWindow(QtWidgets.QMainWindow):
    window = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(500, 500)
        self.setCentralWidget(QtWidgets.QWidget(self))

        menu = self.menuBar()
        file_menu = menu.addMenu("File")

        import_action = QtWidgets.QAction("import json", self)
        import_action.triggered.connect(import_rig_data)

        export_action = QtWidgets.QAction("export json", self)
        export_action.triggered.connect(export_rig_data)

        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        root_layout = QtWidgets.QVBoxLayout()
        root_layout.addWidget(tab_widget)
        self.centralWidget().setLayout(root_layout)

        main_layout = QtWidgets.QHBoxLayout()
        root_layout.addLayout(main_layout)

        hierarchy_group = QtWidgets.QGroupBox("modules")
        hierarchy_layout = QtWidgets.QVBoxLayout()
        hierarchy_group.setLayout(hierarchy_layout)
        main_layout.addWidget(hierarchy_group)

        hierarchy_layout.addWidget(tree_view)
        hierarchy_layout.addWidget(delete_button)

        settings_group = QtWidgets.QGroupBox("module settings")
        settings_layout = QtWidgets.QVBoxLayout()
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        module_layout = QtWidgets.QVBoxLayout()
        module_layout.setAlignment(QtCore.Qt.AlignTop)
        module_layout.addWidget(node_widget)
        module_layout.addWidget(segment_widget)
        module_layout.addWidget(connect_button)
        settings_layout.addLayout(module_layout)

        operation_group = QtWidgets.QGroupBox("operations")
        operation_layout = QtWidgets.QVBoxLayout()
        operation_group.setLayout(operation_layout)
        root_layout.addWidget(operation_group)

        build_layout = QtWidgets.QHBoxLayout()

        build_rig_button = QtWidgets.QPushButton("build")
        build_rig_button.clicked.connect(build_rig)
        build_layout.addWidget(build_rig_button)

        unbuild_rig_button = QtWidgets.QPushButton("unbuild")
        unbuild_rig_button.clicked.connect(build_rig)
        build_layout.addWidget(unbuild_rig_button)

        operation_layout.addLayout(build_layout)


def open_window():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if 'auto_rig' in win.objectName():
                win.destroy()

    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    MainWindow.window = MainWindow(parent=maya_main_window)
    MainWindow.window.setObjectName('auto_rig')
    MainWindow.window.setWindowTitle('Maya Auto Rig')
    MainWindow.window.show()


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        unload_packages(silent=False, packages=["data", "helpers", "logging", "rig", "source", "ui", "utilities"])
    open_window()
