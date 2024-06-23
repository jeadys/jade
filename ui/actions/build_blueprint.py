import maya.cmds as cmds

from modular.components.arm import arm_segments
from modular.components.fingers.thumb_finger import thumb_finger_segments
from modular.components.fingers.index_finger import index_finger_segments
from modular.components.fingers.middle_finger import middle_finger_segments
from modular.components.fingers.ring_finger import ring_finger_segments
from modular.components.fingers.pinky_finger import pinky_finger_segments
from modular.components.toes.index_toe import index_toe_segments
from modular.components.toes.middle_toe import middle_toe_segments
from modular.components.toes.ring_toe import ring_toe_segments
from modular.components.toes.pinky_toe import pinky_toe_segments

from modular.components.leg import leg_segments
from modular.components.spine import spine_segments
from modular.components.front_leg import front_leg_segments
from modular.components.rear_leg import rear_leg_segments
from modular.components.arachne_leg import arachne_leg_segments
from modular.components.wing import wing_segments

from ui.actions.undoable_action import undoable_action

from utilities.curve_from_locators import create_visual_connection
from utilities.enums import Shape, Color

from functools import partial


@undoable_action
def build_blueprint(blueprint_component):
    selection = [obj for obj in cmds.ls(sl=True) if cmds.listRelatives(obj, shapes=True, type="locator")]

    if not cmds.objExists("master"):
        cmds.createNode("network", name="master", skipSelect=True)
        cmds.addAttr("master", niceName="children", longName="children", attributeType="message")

    node = create_blueprint_node(component_type=blueprint_component, selection=selection)

    create_visual_with_defaults = partial(create_blueprint_visual, node=node, selection=selection)
    match blueprint_component:
        case "arm":
            create_visual_with_defaults(segments=arm_segments)
        case "index_toe":
            create_visual_with_defaults(segments=index_toe_segments)
        case "middle_toe":
            create_visual_with_defaults(segments=middle_toe_segments)
        case "ring_toe":
            create_visual_with_defaults(segments=ring_toe_segments)
        case "pinky_toe":
            create_visual_with_defaults(segments=pinky_toe_segments)
        case "thumb_finger":
            create_visual_with_defaults(segments=thumb_finger_segments)
        case "index_finger":
            create_visual_with_defaults(segments=index_finger_segments)
        case "middle_finger":
            create_visual_with_defaults(segments=middle_finger_segments)
        case "ring_finger":
            create_visual_with_defaults(segments=ring_finger_segments)
        case "pinky_finger":
            create_visual_with_defaults(segments=pinky_finger_segments)
        case "leg":
            create_visual_with_defaults(segments=leg_segments)
        case "spine":
            create_visual_with_defaults(segments=spine_segments)
        case "front_leg":
            create_visual_with_defaults(segments=front_leg_segments)
        case "rear_leg":
            create_visual_with_defaults(segments=rear_leg_segments)
        case "arachne_leg":
            create_visual_with_defaults(segments=arachne_leg_segments)
        case "wing":
            create_visual_with_defaults(segments=wing_segments)
        case _:
            create_visual_with_defaults(segments=arm_segments)


def create_blueprint_node(component_type, selection):
    node = cmds.createNode("network", name=f"{component_type}_blueprint_#", skipSelect=True)
    cmds.addAttr(node, niceName="component_type", longName="component_type", dataType="string", readable=False,
                 writable=False,
                 hidden=True)
    cmds.setAttr(f"{node}.component_type", component_type, type="string")
    cmds.addAttr(node, niceName="parent_node", longName="parent_node", attributeType="message", readable=False,
                 writable=True)
    cmds.addAttr(node, niceName="parent_joint", longName="parent_joint", attributeType="message")
    cmds.addAttr(node, niceName="mirror", longName="mirror", attributeType="bool", defaultValue=1)

    cmds.addAttr(node, niceName="stretch", longName="stretch", attributeType="bool", defaultValue=1)
    cmds.addAttr(node, niceName="twist", longName="twist", attributeType="bool", defaultValue=1)
    cmds.addAttr(node, niceName="twist_joints", longName="twist_joints", attributeType="long", minValue=1,
                 maxValue=10, defaultValue=5)
    cmds.addAttr(node, niceName="twist_influence", longName="twist_influence", attributeType="double", minValue=0,
                 maxValue=1, defaultValue=0.75)

    cmds.addAttr(node, niceName="children", longName="children", attributeType="message", readable=True,
                 writable=False)
    cmds.addAttr(node, niceName="segments", longName="segments", attributeType="message", readable=True,
                 writable=False)

    cmds.addAttr(node, niceName="is_built", longName="is_built", attributeType="bool", defaultValue=False,
                 readable=False, writable=False, hidden=True)

    if selection:
        parent_blueprint = cmds.listConnections(f"{selection[0]}.blueprint")[0]
        cmds.connectAttr(f"{selection[0]}.children", f"{node}.parent_joint")
        cmds.connectAttr(f"{parent_blueprint}.children", f"{node}.parent_node")
    else:
        cmds.connectAttr("master.children", f"{node}.parent_node")

    return node


def create_blueprint_visual(segments, node, selection):
    blueprint_nr = node.rsplit("_", 1)[-1]
    for segment in segments:
        current_segment = cmds.spaceLocator(name=f"{segment.name}_#")[0]

        cmds.addAttr(current_segment, niceName="blueprint", longName="blueprint", attributeType="message",
                     readable=True, writable=True)
        cmds.addAttr(current_segment, niceName="parent", longName="parent", attributeType="message", readable=False,
                     writable=True)
        cmds.addAttr(current_segment, niceName="children", longName="children", attributeType="message",
                     readable=True, writable=False)

        if segment.control is not None:
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
            cmds.matchTransform(current_segment, f"{segment.parent.name}_{blueprint_nr}", position=True,
                                rotation=False, scale=False)
            cmds.move(*segment.position, current_segment, relative=True, objectSpace=True)
            cmds.parent(current_segment, f"{segment.parent.name}_{blueprint_nr}")
            create_visual_connection(from_node=f"{segment.parent.name}_{blueprint_nr}",
                                     to_node=current_segment)
        elif segment.parent is None and selection:
            cmds.parent(current_segment, selection[0])
            selection_position = cmds.xform(selection[0], query=True, translation=True, absolute=True,
                                            worldSpace=True)
            cmds.move(*selection_position, current_segment, relative=True, objectSpace=True)
            create_visual_connection(selection[0], to_node=current_segment)
        else:
            cmds.move(*segment.position, current_segment, relative=True, objectSpace=True)

        cmds.connectAttr(f"{node}.segments", f"{current_segment}.blueprint")
