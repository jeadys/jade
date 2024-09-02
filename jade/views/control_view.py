from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QComboBox, QGridLayout, QVBoxLayout, QWidget

from jade.widgets.color_button import ColorButton
from jade.widgets.container import Container
from jade.widgets.labeled_widget import LabeledWidget


class ControlView(QWidget):
    shape_state = Signal(str)
    color_state = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["square", "circle", "triangle"])
        self.shape_combo.currentTextChanged.connect(self.handle_shape_state)

        self.button = ColorButton(color="#ffffff")
        self.button.color_changed.connect(self.handle_color_state)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        control_container = Container("control")
        control_content = QGridLayout(control_container.contentWidget)
        layout.addWidget(control_container)

        # Shape Widget
        shape_widget = LabeledWidget(name="shape")
        shape_widget.addWidget(self.shape_combo)
        control_content.addWidget(shape_widget)

        # Color Widget
        color_widget = LabeledWidget(name="color")
        color_widget.addWidget(self.button)
        control_content.addWidget(color_widget)

    def handle_shape_state(self, state):
        self.shape_state.emit(state)

    def update_shape(self, shape):
        self.shape_combo.blockSignals(True)
        self.shape_combo.setCurrentText(shape)
        self.shape_combo.blockSignals(False)

    def handle_color_state(self, state):
        self.color_state.emit(state)

    def update_color(self, color):
        self.button.setColor(color)
