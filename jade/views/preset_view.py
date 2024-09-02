from PySide2.QtCore import Qt, Signal, QItemSelection
from PySide2.QtGui import QStandardItem, QStandardItemModel
from PySide2.QtWidgets import QListView, QVBoxLayout, QWidget, QLabel
from jade.observers import Publisher


class PresetView(QWidget):
    selection_changed_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.preset_list = QListView()

        model = QStandardItemModel()
        self.preset_list.setModel(model)

        items = ["human", "dog", "spider"]

        for item in items:
            item = QStandardItem(item)
            model.appendRow(item)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)
        self.setFixedHeight(150)

        widget = QWidget()

        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setAlignment(Qt.AlignTop)
        widget.setLayout(widget_layout)

        title = QLabel("presets")
        widget_layout.addWidget(title)
        widget_layout.addWidget(self.preset_list)

        layout.addWidget(widget)

    def on_selection_changed(self, selected):
        if not selected.indexes():
            self.selection_changed_signal.emit(object)
            return

        node = selected.indexes()[0]
        selected_node = node.data(Qt.DisplayRole)
        self.selection_changed_signal.emit(selected_node)

    @staticmethod
    def selection_changed(publisher: Publisher, selected: QItemSelection, deselected: QItemSelection = None):
        if not selected.indexes():
            publisher.selected_node = None
            return

        node = selected.indexes()[0]
        text = node.data(Qt.DisplayRole)

        publisher.selected_node = text
