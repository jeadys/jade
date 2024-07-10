from data.rig_structure import Control, Module, Segment
from rig.modules.biped.spine import create_chain_module
from utilities.enums import Color, Orient, RotateOrder, Shape

wing_upperarm = Segment(
    name="wing_upperarm",
    translateX=0,
    translateY=0,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="wing",
    parent_joint=None,
    children=["wing_lowerarm"],
    control=Control(
        name="wing_upperarm",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control=None,
    )
)

wing_lowerarm = Segment(
    name="wing_lowerarm",
    translateX=5,
    translateY=0,
    translateZ=-10,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="wing",
    parent_joint="wing_upperarm",
    children=["wing_wrist"],
    control=Control(
        name="wing_lowerarm",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control="wing_upperarm",
    )
)

wing_wrist = Segment(
    name="wing_wrist",
    translateX=30,
    translateY=0,
    translateZ=20,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="wing",
    parent_joint="wing_lowerarm",
    children=[""],
    control=Control(
        name="wing_wrist",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control="wing_lowerarm",
    )
)

wing_module = Module(
    name="wing",
    component_type="wing",
    children=[""],
    segments=[wing_upperarm, wing_lowerarm, wing_wrist],
    parent_node=None,
    parent_joint=None,
    mirror=True,
    stretch=True,
    twist=True,
    twist_joints=5,
    twist_influence=0.5
)

wing_fingers = {
    "wing_thumb": {"chain_amount": 4, "rotateY": -75},
    "wing_index": {"chain_amount": 5, "rotateY": -60},
    "wing_middle": {"chain_amount": 5, "rotateY": -45},
    "wing_ring": {"chain_amount": 5, "rotateY": -15},
    "wing_pinky": {"chain_amount": 5, "rotateY": 15}
}

for key, finger_info in wing_fingers.items():
    chain_amount = finger_info["chain_amount"]
    rotateY = finger_info["rotateY"]

    wing_finger = create_chain_module(chain_amount=chain_amount, chain_name=key, max_distance=50)
    wing_finger.parent_node = wing_module.name
    wing_finger.parent_joint = wing_wrist.name
    wing_finger.segments[0].parent_joint = wing_wrist.name
    wing_finger.segments[0].control.parent_control = wing_wrist.name
    wing_finger.segments[0].rotateX = -90
    wing_finger.segments[0].rotateY = rotateY
    wing_module.segments.extend(wing_finger.segments)
