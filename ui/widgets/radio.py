from PySide2 import QtWidgets

from ui.widgets.horizontal import HorizontalWidget
from ui.widgets.label import LabelWidget


def create_radio_button(name: str, options: list[str]):
    widget = HorizontalWidget()
    label = LabelWidget(name)

    widget.layout().addWidget(label)

    button_group = QtWidgets.QButtonGroup()

    for index, radio in enumerate(options):
        radio = QtWidgets.QRadioButton(radio)
        widget.layout().addWidget(radio)
        button_group.addButton(radio)
        button_group.setId(radio, index)
        if index == 0:
            radio.setChecked(True)

    return widget, button_group
