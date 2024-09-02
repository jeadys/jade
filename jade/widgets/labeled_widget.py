from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide2.QtCore import Qt


class LabeledWidget(QWidget):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        label = QLabel(name)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setFixedWidth(75)
        layout.addWidget(label)

    def addWidget(self, widget: QWidget):
        self.layout().addWidget(widget)
