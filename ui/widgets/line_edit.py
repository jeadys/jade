from PySide2 import QtWidgets


def create_line_edit(name: str):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    line_edit = QtWidgets.QLineEdit()
    layout.addWidget(line_edit)

    return widget, line_edit
