from jade.models.maya_model import MayaModel
from jade.observers import Publisher
from jade.views.ribbon_view import RibbonView


class RibbonPresenter:
    def __init__(self, model: MayaModel, view: RibbonView, publisher: Publisher):
        self.model = model
        self.view = view
        self.publisher = publisher
        self.publisher.register_observer(self)

        self.view.ribbon_state.connect(self.handle_ribbon_state)
        self.view.division_count_state.connect(self.handle_division_count_state)
        self.view.tweak_count_state.connect(self.handle_tweak_count_state)

        self.update_view()

    def handle_ribbon_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        self.model.set_node_attr(node=selected_node, attr='is_ribbon_enabled', value=state)

    def handle_division_count_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        if state < 1 or state > 5:
            print("Joint count should be between 1 and 5")
            return

        self.model.set_node_attr(node=selected_node, attr='division_count', value=state)

    def handle_tweak_count_state(self, state):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            return

        if state < 1 or state > 5:
            print("Joint count should be between 1 and 5")
            return

        self.model.set_node_attr(node=selected_node, attr='tweak_count', value=state)

    def update_view(self):
        selected_node = self.publisher.selected_node
        if selected_node is None:
            self.view.setEnabled(False)
            return

        self.view.setEnabled(True)

        is_ribbon_enabled: bool = self.model.get_node_attr(node=selected_node, attr="is_ribbon_enabled")
        self.view.update_is_ribbon_enabled(is_ribbon_enabled)

        division_count: int = self.model.get_node_attr(node=selected_node, attr="division_count")
        self.view.update_division_count(division_count)

        tweak_count: int = self.model.get_node_attr(node=selected_node, attr="tweak_count")
        self.view.update_tweak_count(tweak_count)
