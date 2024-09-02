from jade.views.preset_view import PresetView


class PresetPresenter:
    def __init__(self, view: PresetView):
        self.view = view

        self.view.preset_list.selectionModel().selectionChanged.connect(self.view.on_selection_changed)
