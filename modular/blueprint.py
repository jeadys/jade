import maya.cmds as cmds
from modular.biped.biped import Segment
from utilities.curve_from_locators import create_visual_connection
from utilities.enums import Shape, Color


class Blueprint:
    def __init__(self, component_type, segments: list[Segment], selection):
        self.component_type = component_type
        self.segments = segments
        self.selection = selection
        self.node = None
        self.blueprint_nr = None

    def create_blueprint_node(self):
        node = cmds.createNode("network", name=f"{self.component_type}_blueprint_#", skipSelect=True)
        self.node = node
        self.blueprint_nr = node.rsplit("_", 1)[-1]
        cmds.addAttr(node, niceName="component_type", longName="component_type", dataType="string", readable=False,
                     writable=False,
                     hidden=True)
        cmds.setAttr(f"{node}.component_type", self.component_type, type="string")
        cmds.addAttr(node, niceName="parent_node", longName="parent_node", attributeType="message", readable=False,
                     writable=True)
        cmds.addAttr(node, niceName="parent_joint", longName="parent_joint", attributeType="message")
        cmds.addAttr(node, niceName="mirror", longName="mirror", attributeType="bool", defaultValue=1)
        
        cmds.addAttr(node, niceName="stretch", longName="stretch", attributeType="bool", defaultValue=1)
        cmds.addAttr(node, niceName="twist", longName="twist", attributeType="bool", defaultValue=1)
        cmds.addAttr(node, niceName="twist_joints", longName="twist_joints", attributeType="long", minValue=1, maxValue=10, defaultValue=1)
        cmds.addAttr(node, niceName="twist_influence", longName="twist_influence", attributeType="double", minValue=0, maxValue=1, defaultValue=0.75)

        cmds.addAttr(node, niceName="children", longName="children", attributeType="message", readable=True,
                     writable=False)
        cmds.addAttr(node, niceName="segments", longName="segments", attributeType="message", readable=True,
                     writable=False)

        cmds.addAttr(node, niceName="is_built", longName="is_built", attributeType="bool", defaultValue=False,
                     readable=False, writable=False, hidden=True)

        if self.selection:
            parent_blueprint = cmds.listConnections(f"{self.selection[0]}.blueprint")[0]
            cmds.connectAttr(f"{self.selection[0]}.children", f"{node}.parent_joint")
            cmds.connectAttr(f"{parent_blueprint}.children", f"{node}.parent_node")
        else:
            cmds.connectAttr("master.children", f"{node}.parent_node")

    def create_blueprint_visual(self):
        for segment in self.segments:
            current_segment = cmds.spaceLocator(name=f"{segment.name}_#")[0]

            cmds.addAttr(current_segment, niceName="blueprint", longName="blueprint", attributeType="message",
                         readable=True, writable=True)
            cmds.addAttr(current_segment, niceName="parent", longName="parent", attributeType="message", readable=False,
                         writable=True)
            cmds.addAttr(current_segment, niceName="children", longName="children", attributeType="message",
                         readable=True, writable=False)

            cmds.addAttr(current_segment, longName=segment.name, numberOfChildren=4, attributeType="compound")
            cmds.addAttr(current_segment, longName="control_shape", attributeType="enum",
                         enumName=Shape.enum_to_string_attribute(), defaultValue=segment.control.shape,
                         parent=segment.name)
            cmds.addAttr(current_segment, longName="control_color", attributeType="enum",
                         enumName=Color.enum_to_string_attribute(), defaultValue=0, parent=segment.name)
            cmds.addAttr(current_segment, longName="control_scale", attributeType="float", minValue=1, maxValue=10,
                         defaultValue=segment.control.scale, parent=segment.name)
            cmds.addAttr(current_segment, longName="dummy", attributeType="message", parent=segment.name, hidden=True)

            if segment.parent is not None:
                cmds.matchTransform(current_segment, f"{segment.parent.name}_{self.blueprint_nr}", position=True,
                                    rotation=False, scale=False)
                cmds.move(*segment.position, current_segment, relative=True, objectSpace=True)
                cmds.parent(current_segment, f"{segment.parent.name}_{self.blueprint_nr}")
                create_visual_connection(from_node=f"{segment.parent.name}_{self.blueprint_nr}",
                                         to_node=current_segment)
            elif segment.parent is None and self.selection:
                cmds.parent(current_segment, self.selection[0])
                selection_position = cmds.xform(self.selection[0], query=True, translation=True, absolute=True,
                                                worldSpace=True)
                cmds.move(*selection_position, current_segment, relative=True, objectSpace=True)
                create_visual_connection(self.selection[0], to_node=current_segment)
            else:
                cmds.move(*segment.position, current_segment, relative=True, objectSpace=True)

            cmds.connectAttr(f"{self.node}.segments", f"{current_segment}.blueprint")
