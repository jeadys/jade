from PySide2.QtGui import QColor, QIcon, QPixmap, QStandardItem, QStandardItemModel, QBrush


class TemplateModel:

    def __init__(self):
        self.model = QStandardItemModel()

        self.modules = ["biped_arm", "biped_leg", "biped_spine", "biped_breasts", "biped_buttocks"]

    def populate_model(self):
        for module in self.modules:
            item = QStandardItem(module)
            item.setForeground(QBrush(QColor(255, 0, 255)))
            item.setIcon(QIcon(QPixmap(f":{module}_85.png")))
            self.model.appendRow(item)
