from PySide2 import QtCore, QtGui, QtWidgets

from source.get_source import get_source
from ui.actions.build_module import build_module


class TabWidget(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.addTab(BipedTab(), "Biped")
        self.addTab(FacialTab(), "Facial")
        self.addTab(QuadrupedTab(), "Quadruped")
        self.addTab(CreatureTab(), "Creature")
        self.addTab(ChainTab(), "Chain")
        self.addTab(MiscTab(), "Misc")


class ModuleButton(QtWidgets.QPushButton):
    def __init__(self, module):
        super(ModuleButton, self).__init__()

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setIconSize(QtCore.QSize(36, 36))
        self.setIcon(QtGui.QIcon(get_source(icon=module)))
        self.clicked.connect(lambda: build_module(module=module))


class BipedTab(QtWidgets.QWidget):
    def __init__(self):
        super(BipedTab, self).__init__()
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.setSizeConstraint(QtWidgets.QHBoxLayout.SetMinimumSize)
        tab_layout.setAlignment(QtCore.Qt.AlignLeft)

        arm_module_button = ModuleButton(module="arm")
        leg_module_button = ModuleButton(module="leg")
        spine_module_button = ModuleButton(module="spine")
        foot_module_button = ModuleButton(module="foot")
        hand_module_button = ModuleButton(module="hand")
        head_module_button = ModuleButton(module="head")
        breast_module_button = ModuleButton(module="breasts")
        buttocks_module_button = ModuleButton(module="buttocks")

        tab_layout.addWidget(arm_module_button)
        tab_layout.addWidget(leg_module_button)
        tab_layout.addWidget(spine_module_button)
        tab_layout.addWidget(foot_module_button)
        tab_layout.addWidget(hand_module_button)
        tab_layout.addWidget(head_module_button)
        tab_layout.addWidget(breast_module_button)
        tab_layout.addWidget(buttocks_module_button)

        self.setLayout(tab_layout)


class FacialTab(QtWidgets.QWidget):
    def __init__(self):
        super(FacialTab, self).__init__()
        tab_layout = QtWidgets.QHBoxLayout()
        tab_layout.setSizeConstraint(QtWidgets.QHBoxLayout.SetMinimumSize)
        tab_layout.setAlignment(QtCore.Qt.AlignLeft)

        ear_module_button = ModuleButton(module="ear")
        eye_module_button = ModuleButton(module="eye")
        eyebrow_module_button = ModuleButton(module="eyebrow")
        lips_module_button = ModuleButton(module="lips")
        mouth_module_button = ModuleButton(module="mouth")
        tongue_module_button = ModuleButton(module="tongue")
        nose_module_button = ModuleButton(module="nose")
        face_module_button = ModuleButton(module="face")

        tab_layout.addWidget(face_module_button)
        tab_layout.addWidget(eye_module_button)
        tab_layout.addWidget(eyebrow_module_button)
        tab_layout.addWidget(lips_module_button)
        tab_layout.addWidget(mouth_module_button)
        tab_layout.addWidget(tongue_module_button)
        tab_layout.addWidget(ear_module_button)
        tab_layout.addWidget(nose_module_button)

        self.setLayout(tab_layout)


class QuadrupedTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QtWidgets.QHBoxLayout()
        self.setLayout(tab_layout)


class CreatureTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QtWidgets.QHBoxLayout()
        self.setLayout(tab_layout)


class ChainTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QtWidgets.QHBoxLayout()
        self.setLayout(tab_layout)


class MiscTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        tab_layout = QtWidgets.QHBoxLayout()
        self.setLayout(tab_layout)


tab_widget = TabWidget()
