import maya.cmds as cmds

from PySide2 import QtGui


class SegmentModel:
    def __init__(self):
        self.model = QtGui.QStandardItemModel()

    def update_model(self, module):
        self.model.clear()

        segments = self.get_node_connection(node=module, attr="segments")

        if segments is None:
            return

        previous_segment = None

        for child in segments:
            child_item = QtGui.QStandardItem(child)
            child_item.setIcon(QtGui.QIcon(QtGui.QPixmap(":locator.png")))

            if previous_segment:
                previous_segment.appendRow(child_item)
            else:
                self.model.appendRow(child_item)

            previous_segment = child_item

    @staticmethod
    def set_node_attr(node, attr, value, type=""):
        if node is None:
            cmds.error(f"node: {node} does not exist", noContext=False)

        if not cmds.objExists(node):
            cmds.error(f"node: {node} does not exist", noContext=False)

        if not cmds.attributeQuery(attr, node=node, exists=True):
            cmds.error(f"attribute: {attr} does not exist on node: {node}", noContext=False)

        cmds.setAttr(f"{node}.{attr}", value, type=type)

    @staticmethod
    def get_node_attr(node, attr):
        if not cmds.objExists(node):
            cmds.error(f"node: {node} does not exist", noContext=False)

        if not cmds.attributeQuery(attr, node=node, exists=True):
            cmds.error(f"attribute: {attr} does not exist on node: {node}", noContext=False)

        return cmds.getAttr(f"{node}.{attr}")

    @staticmethod
    def set_node_connection(from_node, from_attr, to_node, to_attr):
        if not cmds.objExists(from_node):
            return cmds.warning(f"node: {from_node} does not exist", noContext=False)

        if not cmds.attributeQuery(from_attr, node=from_node, exists=True):
            return cmds.warning(f"attribute: {from_attr} does not exist on node: {from_node}", noContext=False)

        if not cmds.isConnected(f"{from_node}.{from_attr}", f"{to_node}.{to_attr}"):
            cmds.connectAttr(f"{from_node}.{from_attr}", f"{to_node}.{to_attr}", force=True)

    @staticmethod
    def get_node_connection(node, attr):
        if not cmds.objExists(node):
            return cmds.warning(f"node: {node} does not exist", noContext=False)

        if not cmds.attributeQuery(attr, node=node, exists=True):
            return cmds.warning(f"attribute: {attr} does not exist on node: {node}", noContext=False)

        connections = cmds.listConnections(f"{node}.{attr}")

        if connections:
            return connections
