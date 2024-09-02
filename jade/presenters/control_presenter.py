from jade.models.segment_model import SegmentModel
from jade.observers import Publisher
from jade.views.control_view import ControlView


class ControlPresenter:
    def __init__(self, model: SegmentModel, view: ControlView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        self.publisher.register_observer(self)

        self.view.shape_state.connect(self.handle_shape_state)
        self.view.color_state.connect(self.handle_color_state)

        self.update_view()

    def handle_shape_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        # self.model.set_node_attr(node=selected_node, attr="shape", value=state, type="string")

    def handle_color_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        self.model.set_node_attr(node=selected_node, attr="hex", value=state.name(), type="string")

    def update_view(self):
        selected_node = self.publisher.selected_node

        if selected_node is None:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)

        color = self.model.get_node_attr(node=selected_node, attr="hex")
        self.view.update_color(color)

        # shape = self.model.get_node_attr(node=selected_node, attr="shape")
        self.view.update_shape("circle")
