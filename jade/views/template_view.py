from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QLabel, QListView, QVBoxLayout, QWidget


class TemplateView(QWidget):
    item_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_list = QListView()

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)
        self.setFixedWidth(150)

        widget = QWidget()

        widget_layout = QVBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setAlignment(Qt.AlignTop)
        widget.setLayout(widget_layout)

        title = QLabel("modules")

        widget_layout.addWidget(title)
        widget_layout.addWidget(self.template_list)

        layout.addWidget(widget)

    def on_clicked(self, selected):
        if not selected.isValid():
            self.item_clicked.emit(object)
            return

        selected_node = selected.data(Qt.DisplayRole)
        self.item_clicked.emit(selected_node)
