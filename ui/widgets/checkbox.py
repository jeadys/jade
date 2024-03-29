from PySide2 import QtWidgets


def create_checkbox(name: str, is_checked: bool):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    checkbox = QtWidgets.QCheckBox()
    checkbox.setChecked(is_checked)
    layout.addWidget(checkbox)

    return widget, checkbox
