from jade.models.template_model import TemplateModel
from jade.views.template_view import TemplateView


class TemplatePresenter:
    def __init__(self, model: TemplateModel, view: TemplateView):
        self.model = model
        self.view = view

        self.view.template_list.setModel(self.model.model)

        self.view.template_list.clicked.connect(self.view.on_clicked)

        self.update_view()

    def update_view(self):
        self.model.model.clear()
        self.model.populate_model()
