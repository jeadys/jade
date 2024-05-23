import maya.cmds as cmds

from modular.blueprint import Blueprint

from modular.components.arm import arm_segments
from modular.components.leg import leg_segments
from modular.components.spine import spine_segments
from modular.components.front_leg import front_leg_segments
from modular.components.rear_leg import rear_leg_segments
from modular.components.arachne_leg import arachne_leg_segments
from modular.components.wing import wing_segments

from ui.actions.undoable_action import undoable_action


@undoable_action
def build_blueprint(blueprint_component):
    selection = [obj for obj in cmds.ls(sl=True) if cmds.listRelatives(obj, shapes=True, type="locator")]

    if not cmds.objExists("master"):
        cmds.createNode("network", name="master", skipSelect=True)
        cmds.addAttr("master", niceName="children", longName="children", attributeType="message")

    match blueprint_component:
        case "arm":
            blueprint = Blueprint(component_type="arm", segments=arm_segments(), selection=selection)
        case "leg":
            blueprint = Blueprint(component_type="leg", segments=leg_segments(), selection=selection)
        case "spine":
            blueprint = Blueprint(component_type="spine", segments=spine_segments(), selection=selection)
        case "front_leg":
            blueprint = Blueprint(component_type="front_leg", segments=front_leg_segments(), selection=selection)
        case "rear_leg":
            blueprint = Blueprint(component_type="rear_leg", segments=rear_leg_segments(), selection=selection)
        case "arachne_leg":
            blueprint = Blueprint(component_type="arachne_leg", segments=arachne_leg_segments(), selection=selection)
        case "wing":
            blueprint = Blueprint(component_type="wing", segments=wing_segments(), selection=selection)
        case _:
            print("asdasd")
            blueprint = Blueprint(component_type="arm", segments=arm_segments(), selection=selection)

    blueprint.create_blueprint_node()
    blueprint.create_blueprint_visual()
