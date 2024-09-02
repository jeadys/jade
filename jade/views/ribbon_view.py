from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QCheckBox, QGridLayout, QSpinBox, QVBoxLayout, QWidget

from jade.widgets.container import Container
from jade.widgets.labeled_widget import LabeledWidget


class RibbonView(QWidget):
    ribbon_state = Signal(bool)
    division_count_state = Signal(int)
    tweak_count_state = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_enabled_checkbox = QCheckBox()
        self.is_enabled_checkbox.stateChanged.connect(self.handle_ribbon_state)

        self.division_count_spinbox = QSpinBox()
        self.division_count_spinbox.setRange(1, 5)
        self.division_count_spinbox.valueChanged.connect(self.handle_division_count_state)

        self.tweak_count_spinbox = QSpinBox()
        self.tweak_count_spinbox.setRange(1, 5)
        self.tweak_count_spinbox.valueChanged.connect(self.handle_tweak_count_state)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        ribbon_container = Container("ribbon")
        ribbon_content = QGridLayout(ribbon_container.contentWidget)
        layout.addWidget(ribbon_container)

        # Is Enabled Widget
        is_enabled_widget = LabeledWidget(name="ribbon")
        is_enabled_widget.addWidget(self.is_enabled_checkbox)
        ribbon_content.addWidget(is_enabled_widget)

        # Division Count Widget
        division_count_widget = LabeledWidget(name="division count")
        division_count_widget.addWidget(self.division_count_spinbox)
        ribbon_content.addWidget(division_count_widget)

        # Tweak Count Widget
        tweak_count_widget = LabeledWidget(name="tweak count")
        tweak_count_widget.addWidget(self.tweak_count_spinbox)
        ribbon_content.addWidget(tweak_count_widget)

    def handle_ribbon_state(self, state: bool):
        self.ribbon_state.emit(state)

    def update_is_ribbon_enabled(self, is_enabled: bool):
        self.is_enabled_checkbox.blockSignals(True)
        self.is_enabled_checkbox.setChecked(is_enabled)
        self.is_enabled_checkbox.blockSignals(False)

    def handle_division_count_state(self, state: int):
        self.division_count_state.emit(state)

    def update_division_count(self, division_count: int):
        self.division_count_spinbox.blockSignals(True)
        self.division_count_spinbox.setValue(division_count)
        self.division_count_spinbox.blockSignals(False)

    def handle_tweak_count_state(self, state: int):
        self.tweak_count_state.emit(state)

    def update_tweak_count(self, tweak_count: int):
        self.tweak_count_spinbox.blockSignals(True)
        self.tweak_count_spinbox.setValue(tweak_count)
        self.tweak_count_spinbox.blockSignals(False)
