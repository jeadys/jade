from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QCheckBox, QGridLayout, QSpinBox, QVBoxLayout, QWidget

from jade.widgets.container import Container
from jade.widgets.labeled_widget import LabeledWidget


class TwistView(QWidget):
    twist_state = Signal(bool)
    joint_count_state = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_enabled_checkbox = QCheckBox()
        self.is_enabled_checkbox.stateChanged.connect(self.handle_twist_state)

        self.joint_count_spinbox = QSpinBox()
        self.joint_count_spinbox.setRange(1, 5)
        self.joint_count_spinbox.valueChanged.connect(self.handle_joint_count_state)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        twist_container = Container("twist")
        twist_content = QGridLayout(twist_container.contentWidget)
        layout.addWidget(twist_container)

        # Is Enabled Widget
        is_enabled_widget = LabeledWidget(name="stretch")
        is_enabled_widget.addWidget(self.is_enabled_checkbox)
        twist_content.addWidget(is_enabled_widget)

        # Joint Count Widget
        joint_count_widget = LabeledWidget(name="joint count")
        joint_count_widget.addWidget(self.joint_count_spinbox)
        twist_content.addWidget(joint_count_widget)

    def handle_twist_state(self, state):
        self.twist_state.emit(state)

    def update_is_twist_enabled(self, is_enabled):
        self.is_enabled_checkbox.blockSignals(True)
        self.is_enabled_checkbox.setChecked(is_enabled)
        self.is_enabled_checkbox.blockSignals(False)

    def handle_joint_count_state(self, state):
        self.joint_count_state.emit(state)

    def update_joint_count(self, joint_count):
        self.joint_count_spinbox.blockSignals(True)
        self.joint_count_spinbox.setValue(joint_count)
        self.joint_count_spinbox.blockSignals(False)
