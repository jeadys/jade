import maya.cmds as cmds

from modular.biped.arm import Arm
from modular.biped.leg import Leg
from modular.biped.spine import Spine
from modular.quadruped.front_leg import FrontLeg
from modular.quadruped.rear_leg import RearLeg
from modular.quadruped.arachne_leg import ArachneLeg
from modular.quadruped.wing import Wing

from modular.components.arm import arm_segments
from modular.components.leg import leg_segments
from modular.components.spine import spine_segments
from modular.components.front_leg import front_leg_segments
from modular.components.rear_leg import rear_leg_segments
from modular.components.arachne_leg import arachne_leg_segments
from modular.components.wing import wing_segments

from ui.actions.undoable_action import undoable_action


@undoable_action
def build_rig(blueprint="master"):
    children = cmds.listConnections(f"{blueprint}.children") or []

    for child in children:
        is_built = cmds.getAttr(f"{child}.is_built")
        if is_built:
            continue

        component_type = cmds.getAttr(f"{child}.component_type")
        mirror = cmds.getAttr(f"{child}.mirror")

        match component_type:
            case "arm":
                right_arm = Arm(node=child, segments=arm_segments(), prefix="L_")
                right_arm.generate_arm()
                right_arm.stretch_arm()
                if mirror:
                    left_arm = Arm(node=child, segments=arm_segments(), prefix="R_")
                    left_arm.generate_arm()
                    left_arm.stretch_arm()
            case "leg":
                left_leg = Leg(node=child, segments=leg_segments(), prefix="L_")
                left_leg.generate_leg()
                left_leg.stretch_leg()
                if mirror:
                    right_leg = Leg(node=child, segments=leg_segments(), prefix="R_")
                    right_leg.generate_leg()
                    right_leg.stretch_leg()
            case "spine":
                spine = Spine(node=child, segments=spine_segments())
                spine.generate_spine()
            case "front_leg":
                left_front_leg = FrontLeg(node=child, segments=front_leg_segments(), prefix="L_")
                left_front_leg.generate_front_leg()
                left_front_leg.stretch_front_leg()
                if mirror:
                    right_front_leg = FrontLeg(node=child, segments=front_leg_segments(), prefix="R_")
                    right_front_leg.generate_front_leg()
                    right_front_leg.stretch_front_leg()
            case "rear_leg":
                left_rear_leg = RearLeg(node=child, segments=rear_leg_segments(), prefix="L_")
                left_rear_leg.generate_rear_leg()
                left_rear_leg.stretch_rear_leg()
                if mirror:
                    right_rear_leg = RearLeg(node=child, segments=rear_leg_segments(), prefix="R_")
                    right_rear_leg.generate_rear_leg()
                    right_rear_leg.stretch_rear_leg()
            case "arachne_leg":
                left_arachne_leg = ArachneLeg(node=child, segments=arachne_leg_segments(), prefix="L_")
                left_arachne_leg.generate_arachne_leg()
                left_arachne_leg.stretch_arachne_leg()
                if mirror:
                    right_arachne_leg = ArachneLeg(node=child, segments=arachne_leg_segments(), prefix="R_")
                    right_arachne_leg.generate_arachne_leg()
                    right_arachne_leg.stretch_arachne_leg()
            case "wing":
                left_wing = Wing(node=child, segments=wing_segments(), prefix="L_")
                left_wing.generate_wing()
                if mirror:
                    left_wing = Wing(node=child, segments=wing_segments(), prefix="R_")
                    left_wing.generate_wing()

        cmds.setAttr(f"{child}.is_built", True)
        build_rig(blueprint=child)
