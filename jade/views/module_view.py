from PySide2.QtCore import QItemSelection, Qt, QEvent, Signal
from PySide2.QtWidgets import QAbstractItemView, QTreeView, QVBoxLayout, QWidget, QLabel

from jade.observers import Publisher


class ModuleView(QWidget):
    selection_changed_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.module_tree = QTreeView()
        self.module_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.module_tree.viewport().installEventFilter(self)
        self.module_tree.setHeaderHidden(True)

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

        widget = QWidget()

        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setAlignment(Qt.AlignTop)
        widget.setLayout(widget_layout)

        title = QLabel("structure")

        widget_layout.addWidget(title)
        widget_layout.addWidget(self.module_tree)

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

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            index = self.module_tree.indexAt(event.pos())
            if not index.isValid():
                self.module_tree.clearSelection()
                self.module_tree.clearFocus()
                return True

        return super().eventFilter(source, event)
