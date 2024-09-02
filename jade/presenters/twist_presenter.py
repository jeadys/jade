from jade.models.maya_model import MayaModel
from jade.observers import Publisher
from jade.views.twist_view import TwistView


class TwistPresenter:
    def __init__(self, model: MayaModel, view: TwistView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        self.publisher.register_observer(self)

        self.view.twist_state.connect(self.handle_twist_state)
        self.view.joint_count_state.connect(self.handle_joint_count_state)

        self.update_view()

    def handle_twist_state(self, state: bool):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        self.model.set_node_attr(node=selected_node, attr='is_twist_enabled', value=state)

    def handle_joint_count_state(self, state: int):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        if state < 1 or state > 5:
            print("Joint count should be between 1 and 5")
            return

        self.model.set_node_attr(node=selected_node, attr='joint_count', value=state)

    def update_view(self) -> None:
        selected_node = self.publisher.selected_node
        if selected_node is None:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)

        is_twist_enabled = self.model.get_node_attr(node=selected_node, attr="is_twist_enabled")
        self.view.update_is_twist_enabled(is_twist_enabled)

        joint_count = self.model.get_node_attr(node=selected_node, attr="joint_count")
        self.view.update_joint_count(joint_count)
