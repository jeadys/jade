from jade.models.maya_model import MayaModel
from jade.observers import Publisher
from jade.views.module_view import ModuleView
from PySide2.QtGui import QStandardItem


class ModulePresenter:
    def __init__(self, model: MayaModel, view: ModuleView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher

        self.view.module_tree.setModel(self.model.model)
        self.view.module_tree.selectionModel().selectionChanged.connect(self.view.on_selection_changed)

        self.view.module_tree.selectionModel().selectionChanged.connect(
            lambda selected, deselected: self.view.selection_changed(publisher=self.publisher, selected=selected))

        self.update_view()

    def update_view(self, selected_node=None):
        if not selected_node:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)
        self.model.model.clear()
        self.model.populate_model(node=selected_node)
        self.view.module_tree.expandAll()

    def add_module(self, module):
        self.model.create_node(name=module)
        self.view.module_tree.expandAll()

