from PySide2 import QtWidgets


def create_radio_button(name: str, options: list[str]):
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)

    label = QtWidgets.QLabel(name)
    layout.addWidget(label)

    button_group = QtWidgets.QButtonGroup()
    for index, radio in enumerate(options):
        radio = QtWidgets.QRadioButton(radio)
        layout.addWidget(radio)
        button_group.addButton(radio)
        button_group.setId(radio, index)
        if index == 0:
            radio.setChecked(True)

    return widget, button_group
