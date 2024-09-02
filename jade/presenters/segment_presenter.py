from jade.models.segment_model import SegmentModel
from jade.observers import Publisher
from jade.views.segment_view import SegmentView


class SegmentPresenter:
    def __init__(self, model: SegmentModel, view: SegmentView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher

        self.view.segment_tree.setModel(self.model.model)
        self.view.segment_tree.selectionModel().selectionChanged.connect(
            lambda selected, deselected: self.view.selection_changed(publisher=self.publisher, selected=selected))

        self.update_view()

    def update_view(self, selected_node=None):
        if not selected_node:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)
        self.model.update_model(selected_node)
        self.view.segment_tree.expandAll()
