from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QGridLayout, QLineEdit, QVBoxLayout, QWidget

from jade.widgets.container import Container
from jade.widgets.labeled_widget import LabeledWidget


class RelationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.module_type_line = QLineEdit()
        self.module_type_line.setDisabled(True)

        self.parent_module_line = QLineEdit()
        self.parent_module_line.setDisabled(True)

        self.parent_segment_combo = QComboBox()

        self.setup_view()

    def setup_view(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        relations_container = Container("module relation")
        relations_content = QGridLayout(relations_container.contentWidget)
        layout.addWidget(relations_container)

        # Module Type Widget
        module_type_widget = LabeledWidget(name="module type")
        module_type_widget.addWidget(self.module_type_line)
        relations_content.addWidget(module_type_widget)

        # Module Type Widget
        parent_module_widget = LabeledWidget(name="parent module")
        parent_module_widget.addWidget(self.parent_module_line)
        relations_content.addWidget(parent_module_widget)

        # Module Type Widget
        parent_segment_widget = LabeledWidget(name="connect to")
        parent_segment_widget.addWidget(self.parent_segment_combo)
        relations_content.addWidget(parent_segment_widget)

    def update_module_type(self, module_type: str):
        self.module_type_line.setText(module_type)

    def update_parent_module(self, parent_module: str):
        self.parent_module_line.setText(parent_module)

    def update_parent_segment(self, segments: list[str]):
        self.parent_segment_combo.clear()
        if segments:
            self.parent_segment_combo.addItems(segments)
