from PySide2 import QtCore, QtWidgets

from jade.maya.actions.build_module import build_module


# from ui.widgets.slider import ribbon_divisions_widget, ribbon_tweaks_widget, twist_amount_widget


class ModuleButton(QtWidgets.QPushButton):
    def __init__(self, module):
        super(ModuleButton, self).__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setIconSize(QtCore.QSize(36, 36))
        # self.setIcon(QtGui.QIcon(get_source(icon=module)))
        self.setToolTip(module)
        self.clicked.connect(lambda: build_module(module=module))


class ModuleTab(QtWidgets.QWidget):
    def __init__(self, modules):
        super().__init__()
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.setSizeConstraint(QtWidgets.QHBoxLayout.SetMinimumSize)
        tab_layout.setAlignment(QtCore.Qt.AlignLeft)

        for module in modules:
            module_button = ModuleButton(module=module)
            tab_layout.addWidget(module_button)

        self.setLayout(tab_layout)


def create_modules_tab_group():
    biped_tab = ModuleTab(modules=["arm", "leg", "spine", "foot", "hand", "head", "breasts", "buttocks"])
    facial_tab = ModuleTab(modules=["face", "eye", "eyebrow", "lips", "mouth", "tongue", "ear", "nose"])
    quadruped_tab = ModuleTab(modules=[])
    creature_tab = ModuleTab(modules=[])

    tab = QtWidgets.QTabWidget()
    tab.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
    tab.addTab(biped_tab, "Biped")
    tab.addTab(facial_tab, "Facial")
    tab.addTab(quadruped_tab, "Quadruped")
    tab.addTab(creature_tab, "Creature")

    return tab


tab_widget = create_modules_tab_group()

#
# class BaseTab(QtWidgets.QWidget):
#     def __init__(self):
#         super(BaseTab, self).__init__()
#         self.module_layout = QtWidgets.QVBoxLayout()
#         self.module_layout.setAlignment(QtCore.Qt.AlignTop)
#         self.setLayout(self.module_layout)
#
#     def add_section(self, title, widgets, layout_type=QtWidgets.QVBoxLayout):
#         section_layout = QtWidgets.QVBoxLayout()
#         self.module_layout.addLayout(section_layout)
#
#         container = Container(title)
#         container.collapse()
#         section_layout.addWidget(container)
#
#         content_layout = layout_type(container.contentWidget)
#         content_layout.setSpacing(10)
#
#         for widget in widgets:
#             content_layout.addWidget(widget)
#
#         return container
#
#
# class RelationTab(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.module_layout = QtWidgets.QVBoxLayout()
#         self.module_layout.setAlignment(QtCore.Qt.AlignTop)
#         self.setLayout(self.module_layout)
#
#         self.module_layout.addWidget(node_widget)
#         self.module_layout.addWidget(segment_widget)
#         self.module_layout.addWidget(connect_button)
#
#
# class MechanismTab(BaseTab):
#     def __init__(self):
#         super().__init__()
#
#         twist_widgets = [twist_widget, twist_amount_widget]
#         self.twist_container = self.add_section("Twist", twist_widgets)
#
#         stretch_widgets = [stretch_widget]
#         self.stretch_container = self.add_section("Stretch", stretch_widgets)
#
#         ribbon_widgets = [ribbon_widget, ribbon_divisions_widget, ribbon_tweaks_widget]
#         self.ribbon_container = self.add_section("Ribbon", ribbon_widgets)
#
#
# def create_settings_tab_group():
#     relation_tab = RelationTab()
#     mechanism_tab = MechanismTab()
#
#     tab = QtWidgets.QTabWidget()
#     tab.addTab(relation_tab, "Relations")
#     tab.addTab(mechanism_tab, "Mechanisms")
#
#     return tab
#
#
# settings_tab = create_settings_tab_group()
