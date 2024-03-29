from PySide2 import QtWidgets


def create_combobox(name: str, items: list[str]):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    combobox = QtWidgets.QComboBox()
    layout.addWidget(combobox)
    for item in items:
        combobox.addItem(item)

    return widget, combobox
