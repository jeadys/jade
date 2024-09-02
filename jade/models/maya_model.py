import maya.cmds as cmds

from PySide2 import QtGui


class MayaModel:
    def __init__(self):
        self.model = QtGui.QStandardItemModel()

    def populate_model(self, node, parent_item=None):
        if not cmds.objExists(node):
            return

        children = cmds.listConnections(f"{node}.children") or []

        for child in children:
            child_item = QtGui.QStandardItem(child)
            child_icon = self.get_node_attr(child_item.text(), "module_icon")
            child_item.setIcon(QtGui.QIcon(QtGui.QPixmap(child_icon)))

            if parent_item:
                parent_item.appendRow(child_item)
            else:
                self.model.appendRow(child_item)

            self.populate_model(node=child, parent_item=child_item)

    def create_node(self, name):
        node = cmds.createNode("network", name=name)
        cmds.addAttr(node, niceName="module_icon", longName="module_icon", dataType="string")
        cmds.setAttr(f"{node}.module_icon", f":/{name}_85.png", type="string")

        cmds.addAttr(node, niceName="parent", longName="parent", attributeType="message")
        cmds.addAttr(node, niceName="children", longName="children", attributeType="message")
        cmds.connectAttr(f"spine_01.children", f"{node}.parent")
        self.model.clear()
        self.populate_model(node="human")

    @staticmethod
    def set_node_attr(node, attr, value):
        if node is None:
            cmds.error(f"node: {node} does not exist", noContext=False)

        if not cmds.objExists(node):
            cmds.error(f"node: {node} does not exist", noContext=False)

        if not cmds.attributeQuery(attr, node=node, exists=True):
            cmds.error(f"attribute: {attr} does not exist on node: {node}", noContext=False)

        cmds.setAttr(f"{node}.{attr}", value)

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
