import maya.cmds as cmds

from rig.biped.arm import Arm
from rig.biped.finger import Finger
from rig.quadruped.toe import Toe
from rig.biped.leg import Leg
from rig.biped.spine import Spine
from rig.quadruped.front_leg import FrontLeg
from rig.quadruped.rear_leg import RearLeg
from rig.quadruped.arachne_leg import ArachneLeg
from rig.quadruped.wing import Wing

from rig.components.arm import arm_module
from rig.components.fingers.thumb_finger import thumb_finger_segments
from rig.components.fingers.index_finger import index_finger_segments
from rig.components.fingers.middle_finger import middle_finger_segments
from rig.components.fingers.ring_finger import ring_finger_segments
from rig.components.fingers.pinky_finger import pinky_finger_segments
from rig.components.toes.index_toe import index_toe_segments
from rig.components.toes.middle_toe import middle_toe_segments
from rig.components.toes.ring_toe import ring_toe_segments
from rig.components.toes.pinky_toe import pinky_toe_segments
from rig.components.leg import leg_module
from rig.components.spine import spine_segments
from rig.components.front_leg import front_leg_module
from rig.components.rear_leg import rear_leg_module
from rig.components.arachne_leg import arachne_leg_segments
from rig.components.wing import wing_segments

from helpers.decorators.undoable import undoable_action


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
                left_arm = Arm(node=child, segments=arm_module.segments, prefix="L_")
                left_arm.generate_arm()
                if mirror:
                    right_arm = Arm(node=child, segments=arm_module.segments, prefix="R_")
                    right_arm.generate_arm()
            case "index_toe":
                left_thumb = Toe(node=child, segments=index_toe_segments, prefix="L_")
                left_thumb.generate_toe()
                if mirror:
                    right_thumb = Toe(node=child, segments=index_toe_segments, prefix="R_")
                    right_thumb.generate_toe()
            case "middle_toe":
                left_thumb = Toe(node=child, segments=middle_toe_segments, prefix="L_")
                left_thumb.generate_toe()
                if mirror:
                    right_thumb = Toe(node=child, segments=middle_toe_segments, prefix="R_")
                    right_thumb.generate_toe()
            case "ring_toe":
                left_thumb = Toe(node=child, segments=ring_toe_segments, prefix="L_")
                left_thumb.generate_toe()
                if mirror:
                    right_thumb = Toe(node=child, segments=ring_toe_segments, prefix="R_")
                    right_thumb.generate_toe()
            case "pinky_toe":
                left_thumb = Toe(node=child, segments=pinky_toe_segments, prefix="L_")
                left_thumb.generate_toe()
                if mirror:
                    right_thumb = Toe(node=child, segments=pinky_toe_segments, prefix="R_")
                    right_thumb.generate_toe()
            case "thumb_finger":
                left_thumb = Finger(node=child, segments=thumb_finger_segments, prefix="L_")
                left_thumb.generate_finger()
                if mirror:
                    right_thumb = Finger(node=child, segments=thumb_finger_segments, prefix="R_")
                    right_thumb.generate_finger()
            case "index_finger":
                left_index = Finger(node=child, segments=index_finger_segments, prefix="L_")
                left_index.generate_finger()
                if mirror:
                    right_index = Finger(node=child, segments=index_finger_segments, prefix="R_")
                    right_index.generate_finger()
            case "middle_finger":
                left_middle = Finger(node=child, segments=middle_finger_segments, prefix="L_")
                left_middle.generate_finger()
                if mirror:
                    right_middle = Finger(node=child, segments=middle_finger_segments, prefix="R_")
                    right_middle.generate_finger()
            case "ring_finger":
                left_ring = Finger(node=child, segments=ring_finger_segments, prefix="L_")
                left_ring.generate_finger()
                if mirror:
                    right_ring = Finger(node=child, segments=ring_finger_segments, prefix="R_")
                    right_ring.generate_finger()
            case "pinky_finger":
                left_pinky = Finger(node=child, segments=pinky_finger_segments, prefix="L_")
                left_pinky.generate_finger()
                if mirror:
                    right_pinky = Finger(node=child, segments=pinky_finger_segments, prefix="R_")
                    right_pinky.generate_finger()
            case "leg":
                left_leg = Leg(node=child, segments=leg_module, prefix="L_")
                left_leg.generate_leg()
                if mirror:
                    right_leg = Leg(node=child, segments=leg_module, prefix="R_")
                    right_leg.generate_leg()
            case "spine":
                spine = Spine(node=child, segments=spine_segments)
                spine.generate_spine()
            case "front_leg":
                left_front_leg = FrontLeg(node=child, segments=front_leg_module, prefix="L_")
                left_front_leg.generate_front_leg()
                if mirror:
                    right_front_leg = FrontLeg(node=child, segments=front_leg_module, prefix="R_")
                    right_front_leg.generate_front_leg()
            case "rear_leg":
                left_rear_leg = RearLeg(node=child, segments=rear_leg_module, prefix="L_")
                left_rear_leg.generate_rear_leg()
                if mirror:
                    right_rear_leg = RearLeg(node=child, segments=rear_leg_module, prefix="R_")
                    right_rear_leg.generate_rear_leg()
            case "arachne_leg":
                left_arachne_leg = ArachneLeg(node=child, segments=arachne_leg_segments, prefix="L_")
                left_arachne_leg.generate_arachne_leg()
                if mirror:
                    right_arachne_leg = ArachneLeg(node=child, segments=arachne_leg_segments, prefix="R_")
                    right_arachne_leg.generate_arachne_leg()
            case "wing":
                left_wing = Wing(node=child, segments=wing_segments, prefix="L_")
                left_wing.generate_wing()
                if mirror:
                    left_wing = Wing(node=child, segments=wing_segments, prefix="R_")
                    left_wing.generate_wing()

        cmds.setAttr(f"{child}.is_built", True)
        build_rig(blueprint=child)
