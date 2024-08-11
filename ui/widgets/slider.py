from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAbstractSpinBox, QHBoxLayout, QLabel, QSlider, QSpinBox, QWidget

from ui.widgets.horizontal import HorizontalWidget
from ui.widgets.label import LabelWidget
from ui.widgets.spinbox import SpinBoxWidget


class SliderWidget(QtWidgets.QSlider):

    def __init__(self, value, minimum, maximum):
        super(SliderWidget, self).__init__(QtCore.Qt.Horizontal)

        self.setValue(value)
        self.setMinimum(minimum)
        self.setMaximum(maximum)


def create_slider(name: str, value: int, minimum: int, maximum: int):
    widget = HorizontalWidget()
    label = LabelWidget(name)
    spinbox = SpinBoxWidget(value=value, minimum=minimum, maximum=maximum)
    slider = SliderWidget(value=value, minimum=minimum, maximum=maximum)

    spinbox.editingFinished.connect(lambda: slider.setValue(spinbox.value()))
    slider.valueChanged.connect(lambda: spinbox.setValue(slider.value()))

    widget.layout().addWidget(label)
    widget.layout().addWidget(spinbox)
    widget.layout().addWidget(slider)

    return widget, spinbox, slider


def create_spinbox_slider(name: str, value: int, minimum: int, maximum: int) -> tuple[QWidget, QSpinBox, QSlider]:
    widget = QWidget()

    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    label = QLabel(name)
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    label.setFixedWidth(75)

    spinbox = QSpinBox()
    spinbox.setValue(value)
    spinbox.setMinimum(minimum)
    spinbox.setMaximum(maximum)
    spinbox.setFixedWidth(75)
    spinbox.setFocusPolicy(Qt.StrongFocus)
    spinbox.wheelEvent = lambda event: None
    spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

    slider = QSlider(Qt.Horizontal)
    slider.setValue(value)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)

    spinbox.valueChanged.connect(lambda: slider.setValue(spinbox.value()))
    slider.valueChanged.connect(lambda: spinbox.setValue(slider.value()))

    layout.addWidget(label)
    layout.addWidget(spinbox)
    layout.addWidget(slider)

    return widget, spinbox, slider
