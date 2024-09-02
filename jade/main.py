from maya import OpenMayaUI
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

from jade import unload_packages
from jade.models.maya_model import MayaModel
from jade.models.segment_model import SegmentModel
from jade.models.template_model import TemplateModel
from jade.observers import Publisher
from jade.presenters.control_presenter import ControlPresenter
from jade.presenters.module_presenter import ModulePresenter
from jade.presenters.preset_presenter import PresetPresenter
from jade.presenters.relation_presenter import RelationPresenter
from jade.presenters.ribbon_presenter import RibbonPresenter
from jade.presenters.segment_presenter import SegmentPresenter
from jade.presenters.template_presenter import TemplatePresenter
from jade.presenters.stretch_presenter import StretchPresenter
from jade.presenters.twist_presenter import TwistPresenter
from jade.views.control_view import ControlView
from jade.views.module_view import ModuleView
from jade.views.preset_view import PresetView
from jade.views.relation_view import RelationView
from jade.views.ribbon_view import RibbonView
from jade.views.segment_view import SegmentView
from jade.views.stretch_view import StretchView
from jade.views.template_view import TemplateView
from jade.views.twist_view import TwistView


class SettingTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.layout)

    def addWidget(self, widget):
        self.layout.addWidget(widget)


class MainWindow(QtWidgets.QMainWindow):
    window = None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.resize(750, 500)
        self.setCentralWidget(QtWidgets.QWidget(self))

        self.module_publisher = Publisher()
        self.segment_publisher = Publisher()

        root_layout = QtWidgets.QVBoxLayout()
        # root_layout.addWidget(tab_widget)
        self.centralWidget().setLayout(root_layout)

        main_layout = QtWidgets.QHBoxLayout()
        root_layout.addLayout(main_layout)

        rig_layout = QtWidgets.QVBoxLayout()

        settings_layout = QtWidgets.QVBoxLayout()
        settings_layout.setAlignment(QtCore.Qt.AlignTop)

        maya_model = MayaModel()
        segment_model = SegmentModel()

        self.preset_view = PresetView()
        self.preset_presenter = PresetPresenter(view=self.preset_view)

        self.module_view = ModuleView()
        self.module_presenter = ModulePresenter(model=maya_model, view=self.module_view,
                                                publisher=self.module_publisher)

        self.template_model = TemplateModel()
        self.template_view = TemplateView()
        self.template_presenter = TemplatePresenter(model=self.template_model, view=self.template_view)

        main_layout.addWidget(self.template_view)
        main_layout.addLayout(rig_layout)

        rig_layout.addWidget(self.preset_view)
        rig_layout.addWidget(self.module_view)

        main_layout.addLayout(settings_layout)

        # Module Settings Widget
        self.label = QtWidgets.QLabel("settings")
        settings_layout.addWidget(self.label)
        self.module_setting_tab_widget = QtWidgets.QTabWidget()
        settings_layout.addWidget(self.module_setting_tab_widget)

        # Relation Settings Tab
        relation_tab = SettingTab(parent=self)

        self.relation_view = RelationView()
        self.relation_presenter = RelationPresenter(model=maya_model, view=self.relation_view,
                                                    publisher=self.module_publisher)
        relation_tab.addWidget(self.relation_view)

        self.module_setting_tab_widget.addTab(relation_tab, "relations")

        # Mechanism Settings Tab
        mechanism_tab = SettingTab(parent=self)

        self.twist_view = TwistView()
        self.twist_presenter = TwistPresenter(model=maya_model, view=self.twist_view, publisher=self.module_publisher)
        mechanism_tab.addWidget(self.twist_view)

        self.stretch_view = StretchView()
        self.stretch_presenter = StretchPresenter(model=maya_model, view=self.stretch_view,
                                                  publisher=self.module_publisher)
        mechanism_tab.addWidget(self.stretch_view)

        self.ribbon_view = RibbonView()
        self.ribbon_presenter = RibbonPresenter(model=maya_model, view=self.ribbon_view,
                                                publisher=self.module_publisher)
        mechanism_tab.addWidget(self.ribbon_view)

        self.module_setting_tab_widget.addTab(mechanism_tab, "mechanisms")

        # Segment Settings Tab
        segment_tab = SettingTab(parent=self)

        self.segment_view = SegmentView()
        self.segment_presenter = SegmentPresenter(model=segment_model, view=self.segment_view,
                                                  publisher=self.segment_publisher)
        self.template_view.item_clicked.connect(self.module_presenter.add_module)

        self.module_view.selection_changed_signal.connect(self.segment_presenter.update_view)
        self.preset_view.selection_changed_signal.connect(self.module_presenter.update_view)

        segment_tab.addWidget(self.segment_view)

        self.control_view = ControlView()
        self.control_presenter = ControlPresenter(model=segment_model, view=self.control_view,
                                                  publisher=self.segment_publisher)

        segment_tab.addWidget(self.control_view)

        self.module_setting_tab_widget.addTab(segment_tab, "segments")

        # Manual sync Model > View
        self.button_update_from_maya = QtWidgets.QPushButton("Manual Sync", self)
        self.button_update_from_maya.clicked.connect(self.manual_sync)
        settings_layout.addWidget(self.button_update_from_maya)

        # main_layout = QtWidgets.QHBoxLayout()
        # root_layout = QtWidgets.QVBoxLayout()
        # menu = self.menuBar()
        # file_menu = menu.addMenu("File")
        #
        # import_action = QtWidgets.QAction("import json", self)
        # import_action.triggered.connect(import_rig_data)
        #
        # export_action = QtWidgets.QAction("export json", self)
        # export_action.triggered.connect(export_rig_data)
        #
        # file_menu.addAction(import_action)
        # file_menu.addAction(export_action)
        #
        # mechanism_tab = SettingTab(parent=self)
        # self.stack_widget = QtWidgets.QStackedWidget()
        # self.stack_widget.addWidget(self.twist_view)
        # self.stack_widget.addWidget(self.stretch_view)
        # mechanism_tab.addWidget(self.stack_widget)
        #
        # hierarchy_group = QtWidgets.QGroupBox("modules")
        # hierarchy_group.setMinimumWidth(300)
        # hierarchy_layout = QtWidgets.QVBoxLayout()
        # hierarchy_group.setLayout(hierarchy_layout)
        # main_layout.addWidget(hierarchy_group)
        #
        # hierarchy_layout.addWidget(tree_widget)
        # hierarchy_layout.addWidget(refresh_button)
        #
        # main_layout.addWidget(setting_group)
        #
        # operation_group = QtWidgets.QGroupBox("operations")
        # operation_layout = QtWidgets.QVBoxLayout()
        # operation_group.setLayout(operation_layout)
        # root_layout.addWidget(operation_group)
        #
        # build_layout = QtWidgets.QHBoxLayout()
        #
        # build_rig_button = QtWidgets.QPushButton("build")
        # build_rig_button.clicked.connect(build_rig)
        # build_layout.addWidget(build_rig_button)
        #
        # unbuild_rig_button = QtWidgets.QPushButton("unbuild")
        # unbuild_rig_button.clicked.connect(build_rig)
        # build_layout.addWidget(unbuild_rig_button)
        #
        # operation_layout.addLayout(build_layout)

    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         index = self.module_tree.indexAt(event.pos())
    #         if not index.isValid():
    #             self.module_tree.clearSelection()
    #             self.module_tree.clearFocus()
    #             return True
    #
    #     return super().eventFilter(source, event)
    #
    # def selection_changed(self, publisher: Publisher, new_node: QItemSelection):
    #
    #     if not new_node.indexes():
    #         publisher.selected_node = None
    #         return
    #
    #     node = new_node.indexes()[0]
    #     text = node.data(Qt.DisplayRole)
    #
    #     publisher.selected_node = text

    def manual_sync(self):
        self.module_publisher.notify_observers()
        self.segment_publisher.notify_observers()


def open_window():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if "Jade" in win.objectName():
                win.destroy()

    maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)
    MainWindow.window = MainWindow(parent=maya_main_window)
    MainWindow.window.setObjectName("Jade")
    MainWindow.window.setWindowTitle("Jade")
    MainWindow.window.show()


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        unload_packages.unload_packages(silent=False,
                                        packages=["views", "presenters", "models", "widgets", "maya", "icons"])

    success = QtCore.QResource.registerResource(
        "C:\\Users\\Realm\\Desktop\\programming\\maya\\jade\\jade\\icons\\resources.rcc")

    print(success)

    exist = QtCore.QFile.exists(":biped_arm_85.png")
    print(exist)
    open_window()
