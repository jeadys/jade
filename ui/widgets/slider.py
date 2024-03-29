from PySide2 import QtWidgets, QtCore


def create_slider(name: str, value: int, minimum: int, maximum: int):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    slider.setValue(value)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)

    spinbox = QtWidgets.QSpinBox()
    spinbox.setValue(value)
    spinbox.setMinimum(minimum)
    spinbox.setMaximum(maximum)

    slider.valueChanged.connect(spinbox.setValue)
    spinbox.valueChanged.connect(slider.setValue)

    layout.addWidget(spinbox)
    layout.addWidget(slider)

    return widget, slider
