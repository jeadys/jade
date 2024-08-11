from PySide2 import QtWidgets, QtCore


class LabelWidget(QtWidgets.QLabel):
    def __init__(self, name):
        super().__init__(name)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.setFixedWidth(75)
