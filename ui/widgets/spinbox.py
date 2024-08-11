from PySide2 import QtCore, QtWidgets

from ui.widgets.horizontal import HorizontalWidget
from ui.widgets.label import LabelWidget


class SpinBoxWidget(QtWidgets.QSpinBox):

    def __init__(self, value, minimum, maximum):
        super(SpinBoxWidget, self).__init__()

        self.setValue(value)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setFixedWidth(75)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.wheelEvent = lambda event: None
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)


def create_spinbox(name: str, value: int, minimum: int, maximum: int) -> object:
    widget = HorizontalWidget()

    label = LabelWidget(name=name)
    spinbox = SpinBoxWidget(value=value, minimum=minimum, maximum=maximum)

    widget.layout().addWidget(label, 0, 0)
    widget.layout().addWidget(spinbox, 0, 1)

    return widget, spinbox
