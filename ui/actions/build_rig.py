import maya.cmds as cmds

from helpers.decorators.undoable_action import undoable_action
from rig.modules.biped.arm import Arm, arm_module
from rig.modules.biped.leg import Leg, leg_module
from rig.modules.biped.spine import create_chain_module, Spine
from rig.modules.creature.arachne_leg import arachne_leg_module, ArachneLeg
from rig.modules.creature.wing import Wing, wing_module
from rig.modules.quadruped.front_leg import front_leg_module, FrontLeg
from rig.modules.quadruped.rear_leg import rear_leg_module, RearLeg
from rig.modules.rig_module import RigModule


@undoable_action
def build_rig(blueprint="master"):
    children = cmds.listConnections(f"{blueprint}.children") or []

    for child in children:
        is_built = cmds.getAttr(f"{child}.is_built")
        if is_built:
            continue

        mirror = cmds.getAttr(f"{child}.mirror")

        left_module: RigModule = build_module(child=child, prefix="L_")
        left_module.generate_module()
        if mirror:
            right_module: RigModule = build_module(child=child, prefix="R_")
            right_module.generate_module()

        cmds.setAttr(f"{child}.is_built", True)
        build_rig(blueprint=child)


def build_module(child, prefix) -> RigModule:
    module_type = cmds.getAttr(f"{child}.module_type")

    segments = cmds.listConnections(f"{child}.segments")

    match module_type:
        case "arm":
            return Arm(node=child, segments=segments, prefix=prefix)
        case "leg":
            return Leg(node=child, segments=segments, prefix=prefix)
        case "spine":
            return Spine(node=child, segments=segments)
        case "front_leg":
            return FrontLeg(node=child, segments=segments, prefix=prefix)
        case "rear_leg":
            return RearLeg(node=child, segments=segments, prefix=prefix)
        case "arachne_leg":
            return ArachneLeg(node=child, segments=segments, prefix=prefix)
        case "wing":
            return Wing(node=child, segments=segments, prefix=prefix)
