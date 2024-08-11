import maya.cmds as cmds
from ui.widgets.tree_widget import tree_widget


def set_attribute(attribute, value):
    module = tree_widget.selectedItems()
    if module:
        cmds.setAttr(f"{module[0].text(0)}.{attribute}", value)
