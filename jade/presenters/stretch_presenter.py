from jade.models.maya_model import MayaModel
from jade.observers import Publisher
from jade.views.stretch_view import StretchView


class StretchPresenter:
    def __init__(self, model: MayaModel, view: StretchView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        self.publisher.register_observer(self)

        self.view.stretch_state.connect(self.handle_stretch_state)

        self.update_view()

    def handle_stretch_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        self.model.set_node_attr(node=selected_node, attr='is_stretch_enabled', value=state)

    def update_view(self):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)

        is_stretch_enabled = self.model.get_node_attr(node=selected_node, attr="is_stretch_enabled")
        self.view.update_is_stretch_enabled(is_stretch_enabled)
