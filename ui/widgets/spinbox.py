from PySide2 import QtWidgets


def create_spinbox(name: str, value: int, minimum: int, maximum: int):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    spinbox = QtWidgets.QSpinBox()
    spinbox.setValue(value)
    spinbox.setMinimum(minimum)
    spinbox.setMaximum(maximum)
    layout.addWidget(spinbox)

    return widget, spinbox
