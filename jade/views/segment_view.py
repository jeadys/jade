from PySide2.QtCore import QItemSelection, Qt, QEvent
from PySide2.QtWidgets import QAbstractItemView, QTreeView, QVBoxLayout, QWidget

from jade.observers import Publisher


class SegmentView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.segment_tree = QTreeView()
        self.segment_tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.segment_tree.viewport().installEventFilter(self)
        self.segment_tree.setHeaderHidden(True)

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

        widget_layout.addWidget(self.segment_tree)

        layout.addWidget(widget)

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
            index = self.segment_tree.indexAt(event.pos())
            if not index.isValid():
                self.segment_tree.clearSelection()
                self.segment_tree.clearFocus()
                return True

        return super().eventFilter(source, event)
