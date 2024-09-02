from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QCheckBox, QGridLayout, QVBoxLayout, QWidget

from jade.widgets.container import Container
from jade.widgets.labeled_widget import LabeledWidget


class StretchView(QWidget):
    stretch_state = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_enabled_checkbox = QCheckBox()
        self.is_enabled_checkbox.stateChanged.connect(self.handle_stretch_state)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        stretch_container = Container("stretch")
        stretch_content = QGridLayout(stretch_container.contentWidget)
        layout.addWidget(stretch_container)

        # Is Enabled Widget
        is_enabled_widget = LabeledWidget(name="stretch")
        is_enabled_widget.addWidget(self.is_enabled_checkbox)
        stretch_content.addWidget(is_enabled_widget)

    def handle_stretch_state(self, state):
        self.stretch_state.emit(state)

    def update_is_stretch_enabled(self, is_enabled):
        self.is_enabled_checkbox.blockSignals(True)
        self.is_enabled_checkbox.setChecked(is_enabled)
        self.is_enabled_checkbox.blockSignals(False)
