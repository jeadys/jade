import maya.cmds as cmds

from helpers.decorators.undoable_action import undoable_action
from rig.modules.biped.arm import Arm
from rig.modules.biped.leg import Leg
from rig.modules.biped.spine import Spine
from rig.modules.creature.arachne_leg import ArachneLeg
from rig.modules.creature.wing import Wing
from rig.modules.quadruped.front_leg import FrontLeg
from rig.modules.quadruped.rear_leg import RearLeg
from rig.modules.rig_module import RigModule


@undoable_action
def build_rig(module="master"):
    children = cmds.listConnections(f"{module}.children") or []

    for child in children:
        is_built = cmds.getAttr(f"{child}.is_built")
        if is_built:
            build_rig(module=child)
            continue

        rig_module: RigModule = build_module(child=child)
        rig_module.generate_module()

        cmds.setAttr(f"{child}.is_built", True)
        build_rig(module=child)


def build_module(child) -> RigModule:
    module_type = cmds.getAttr(f"{child}.module_type")

    segments = cmds.listConnections(f"{child}.segments")

    match module_type:
        case "arm":
            return Arm(node=child, segments=segments)
        case "leg":
            return Leg(node=child, segments=segments)
        case "spine":
            return Spine(node=child, segments=segments)
        case "front_leg":
            return FrontLeg(node=child, segments=segments)
        case "rear_leg":
            return RearLeg(node=child, segments=segments)
        case "arachne_leg":
            return ArachneLeg(node=child, segments=segments)
        case "wing":
            return Wing(node=child, segments=segments)
