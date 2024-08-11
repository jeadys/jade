from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QWidget

from ui.widgets.set_attribute import set_attribute


class CheckBoxWidget(QtWidgets.QCheckBox):
    def __init__(self, name: str, is_checked: bool):
        super().__init__()
        self.setChecked(is_checked)
        self.setToolTip(name)


def create_checkbox(name: str, is_checked: bool):
    widget = QWidget()

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    label = QLabel(name)
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    label.setFixedWidth(75)

    checkbox = QCheckBox()
    checkbox.setChecked(is_checked)

    layout.addWidget(label)
    layout.addWidget(checkbox)

    return widget, checkbox


twist_widget, twist_checkbox = create_checkbox(name="add twist", is_checked=True)
stretch_widget, stretch_checkbox = create_checkbox(name="add stretch", is_checked=True)
ribbon_widget, ribbon_checkbox = create_checkbox(name="add ribbon", is_checked=True)

twist_checkbox.stateChanged.connect(lambda: set_attribute("twist_enabled", twist_checkbox.isChecked()))
stretch_checkbox.stateChanged.connect(lambda: set_attribute("stretch_enabled", stretch_checkbox.isChecked()))
ribbon_checkbox.stateChanged.connect(lambda: set_attribute("ribbon_enabled", ribbon_checkbox.isChecked()))
