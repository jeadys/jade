import maya.cmds as cmds
from PySide2 import QtWidgets

from ui.actions.refresh_ui import refresh_ui
from ui.widgets.combobox import node_combobox, segment_combobox
from ui.widgets.tree_widget import tree_widget
from utilities.check_relation import has_parent


def parent_module_to_selected_module():
    selected_items = tree_widget.selectedItems()

    if not selected_items:
        cmds.warning(f"Select a module in the tree view", noContext=False)
        return

    selected_module = selected_items[0].text(0)
    parent_node = node_combobox.currentText()
    parent_joint = segment_combobox.currentText()

    if selected_module == parent_node:
        cmds.warning(f"{selected_module} can not be parented to itself", noContext=False)
        return

    selected_module_children = cmds.listConnections(f"{selected_module}.children") or []
    selected_module_parent_node = cmds.listConnections(f"{selected_module}.parent_node") or []
    selected_module_parent_joint = cmds.listConnections(f"{selected_module}.parent_joint") or []

    if parent_node in selected_module_children:
        cmds.warning(f"Cannot parent {selected_module} to one of its children: {parent_node}", noContext=False)
        return

    if parent_node in selected_module_parent_node and parent_joint in selected_module_parent_joint:
        cmds.warning(f"{selected_module} is already parented to {parent_node} - {parent_joint}", noContext=False)
        return

    if not parent_joint and not selected_module_parent_joint:
        cmds.warning(f"{selected_module} is already parented to the world", noContext=False)
        return

    root_segment = cmds.listConnections(f"{selected_module}.segments[0]", destination=True, plugs=False)[0]

    if not cmds.isConnected(f"{parent_node}.children", f"{selected_module}.parent_node"):
        cmds.connectAttr(f"{parent_node}.children", f"{selected_module}.parent_node", force=True)

    if parent_node == "master":
        cmds.disconnectAttr(f"{selected_module_parent_joint[0]}.children", f"{selected_module}.parent_joint")

        if not has_parent(from_parent=root_segment, to_parent=None):
            cmds.parent(root_segment, world=True)
    else:
        if not cmds.isConnected(f"{parent_joint}.children", f"{selected_module}.parent_joint"):
            cmds.connectAttr(f"{parent_joint}.children", f"{selected_module}.parent_joint", force=True)


        if not has_parent(from_parent=root_segment, to_parent=parent_joint):
            cmds.parent(root_segment, parent_joint)

        cmds.matchTransform(root_segment, parent_joint, position=True, rotation=True, scale=False)

    tree_widget.move_item(parent_node)
    refresh_ui(tree=tree_widget, combobox=node_combobox)


connect_button = QtWidgets.QPushButton("connect module")
connect_button.clicked.connect(parent_module_to_selected_module)
