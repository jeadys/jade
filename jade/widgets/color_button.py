from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPushButton


class ColorButton(QPushButton):
    color_changed = Signal(object)

    def __init__(self, *args, color=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._color = None
        self._default = color
        self.clicked.connect(self.onColorPicker)

        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.color_changed.emit(color)

        if self._color:
            self.setStyleSheet(f"background-color: {self._color};")
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        color_dialog = QtWidgets.QColorDialog()
        if self._color:
            color_dialog.setCurrentColor(QtGui.QColor(self._color))

        if color_dialog.exec_():
            self.setColor(color_dialog.currentColor().name())
