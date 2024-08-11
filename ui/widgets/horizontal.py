from PySide2 import QtWidgets


class HorizontalWidget(QtWidgets.QWidget):
    def __init__(self):
        super(HorizontalWidget, self).__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
