from jade.models.maya_model import MayaModel
from jade.observers import Publisher
from jade.views.relation_view import RelationView


class RelationPresenter:
    def __init__(self, model: MayaModel, view: RelationView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        self.publisher.register_observer(self)

        self.update_view()

    def update_view(self):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)

        module_type = self.model.get_node_attr(node=selected_node, attr="module_type")
        self.view.update_module_type(module_type)

        parent_module = self.model.get_node_connection(node=selected_node, attr="parent")
        if parent_module:
            self.view.update_parent_module(parent_module[0])
            segments = self.model.get_node_connection(node=parent_module[0], attr="segments")
            self.view.update_parent_segment(segments=segments)
