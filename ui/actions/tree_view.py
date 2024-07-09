from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
from ui.widgets.combobox import create_combobox


class StandardItem(QtGui.QStandardItem):
    def __init__(self, text, font_size):
        super(StandardItem, self).__init__()

        self.setEditable(False)
        self.setText(text)
        self.setFont(QtGui.QFont("Open Sans", font_size))


class TreeView(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        self.model = QtGui.QStandardItemModel()
        self.model.invisibleRootItem()
        self.setHeaderHidden(True)
        self.setModel(self.model)
        self.undo_stack = QtWidgets.QUndoStack(self)
        self.items_map = {}

    def add_item(self, name: str, item: StandardItem, parent_name):
        if self.find_item(name):
            return

        self.items_map[name] = item

        item = self.items_map[name]
        if parent_name and parent_name != "master":
            parent_item = self.items_map[parent_name]
            parent_item.appendRow(item)
        else:
            tree_view.model.appendRow(item)

    def remove_item(self):
        selection_model = self.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if selected_indexes:
            selected_index = selected_indexes[0]
            selected_name = selected_index.data()
            self.model.removeRow(selected_index.row(), selected_index.parent())

            found_index = node_combobox.findText(selected_name)
            node_combobox.removeItem(found_index)

    def find_item(self, search: str):
        items = self.model.findItems(search, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive, 0)
        if items:
            return items[0]
        return None

    def move_item(self, selected_node):
        selection_model = self.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if not selected_indexes or len(selected_indexes) > 1:
            return

        source_index = selected_indexes[0]
        source_item = self.model.itemFromIndex(source_index)
        source_row = source_index.row()
        source_parent = source_item.parent()

        # Find the destination parent based on selected_parent_name
        # Determine the destination parent based on selected_parent_name
        if selected_node == "master":
            destination_parent = self.model.invisibleRootItem()
        else:
            destination_parent = self.find_item(search=selected_node)

        if not source_item or not destination_parent:
            return

        # If the source parent is the same as the destination parent, no need to move
        if source_parent == destination_parent:
            return

        # If the source item has a parent, remove it from the source parent
        if source_parent:
            source_parent.takeRow(source_row)
        else:
            # Handle the case where source_item is at the root level
            root_item = self.model.invisibleRootItem()
            root_item.takeRow(source_row)

        # Add to the destination parent
        if destination_parent:
            destination_row = destination_parent.rowCount()
            destination_parent.insertRow(destination_row, source_item)


tree_view = TreeView()

connect_button = QtWidgets.QPushButton("connect")
delete_button = QtWidgets.QPushButton("delete")

node_widget, node_combobox = create_combobox(name="Parent Module", items=["master"])
segment_widget, segment_combobox = create_combobox(name="Parent Joint", items=[])


def has_connection(from_connection, to_connection):
    is_connected = cmds.isConnected(from_connection, to_connection)
    return is_connected


def has_parent(from_parent, to_parent=None):
    current_parent = cmds.listRelatives(from_parent, parent=True)

    if to_parent is None:
        return current_parent is None

    return current_parent and current_parent[0] == to_parent


def delete_module_selection():
    index = tree_view.currentIndex()
    selected_module = tree_view.model.data(index)

    segments = cmds.listConnections(f"{selected_module}.segments", destination=True, plugs=False)
    if segments:
        cmds.delete(segments[0])

    tree_view.remove_item()


def parent_module_to_selection():
    index = tree_view.currentIndex()
    selected_module = tree_view.model.data(index)

    if not selected_module:
        cmds.warning(f"Select a module in the tree view", noContext=False)
        return

    parent_node = node_combobox.currentText()
    parent_joint = segment_combobox.currentText()

    if selected_module == parent_node:
        cmds.warning(f"{selected_module} can not be parented to itself", noContext=False)
        return

    selected_module_children = cmds.listConnections(f"{selected_module}.children") or []
    previous_parent_node = cmds.listConnections(f"{selected_module}.parent_node") or []
    previous_parent_joint = cmds.listConnections(f"{selected_module}.parent_joint") or []

    if parent_node in selected_module_children:
        cmds.warning(f"Cannot parent {selected_module} to one of its children: {parent_node}", noContext=False)
        return

    if parent_node in previous_parent_node and parent_joint in previous_parent_joint:
        cmds.warning(f"{selected_module} is already parented to {parent_node} - {parent_joint}", noContext=False)
        return

    if not parent_joint and not previous_parent_joint:
        cmds.warning(f"{selected_module} is already parented to the world", noContext=False)
        return

    root_segment = cmds.listConnections(f"{selected_module}.segments[0]", destination=True, plugs=False)[0]

    if not cmds.isConnected(f"{parent_node}.children", f"{selected_module}.parent_node"):
        cmds.connectAttr(f"{parent_node}.children", f"{selected_module}.parent_node", force=True)

    if parent_node != "master":
        if not cmds.isConnected(f"{parent_joint}.children", f"{selected_module}.parent_joint"):
            cmds.connectAttr(f"{parent_joint}.children", f"{selected_module}.parent_joint", force=True)

        if not cmds.isConnected(f"{parent_joint}.children", f"{root_segment}.parent_joint"):
            cmds.connectAttr(f"{parent_joint}.children", f"{root_segment}.parent_joint", force=True)

        if not has_parent(root_segment, parent_joint):
            cmds.parent(root_segment, parent_joint)

        cmds.matchTransform(root_segment, parent_joint, position=True, rotation=True, scale=False)
    else:
        cmds.disconnectAttr(f"{previous_parent_joint[0]}.children", f"{selected_module}.parent_joint")
        cmds.disconnectAttr(f"{previous_parent_joint[0]}.children", f"{root_segment}.parent_joint")

        if not has_parent(root_segment):
            cmds.parent(root_segment, world=True)

    tree_view.move_item(parent_node)


connect_button.clicked.connect(parent_module_to_selection)
delete_button.clicked.connect(delete_module_selection)


def display_module_parents_in_combobox(index):
    model = index.model()
    selected_module = model.data(index)
    cmds.select(selected_module)

    parent_node = cmds.listConnections(f"{selected_module}.parent_node")
    parent_joint = cmds.listConnections(f"{selected_module}.parent_joint")

    node_combobox.setCurrentText(parent_node[0]) if parent_node else node_combobox.setCurrentText("")
    segment_combobox.setCurrentText(parent_joint[0]) if parent_joint else segment_combobox.setCurrentText("")


tree_view.clicked.connect(display_module_parents_in_combobox)
