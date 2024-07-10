from data.rig_structure import Control, Module, Segment
from utilities.enums import Color, Orient, RotateOrder, Shape

clavicle = Segment(
    name="clavicle",
    translateX=5,
    translateY=140,
    translateZ=5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arm",
    parent_joint=None,
    children=["upperarm"],
    control=Control(
        name="clavicle",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control=None,
    )
)

upperarm = Segment(
    name="upperarm",
    translateX=10,
    translateY=0,
    translateZ=-15,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arm",
    parent_joint="clavicle",
    children=["lowerarm"],
    control=Control(
        name="upperarm",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="clavicle",
    )
)

lowerarm = Segment(
    name="lowerarm",
    translateX=30,
    translateY=0,
    translateZ=-7.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arm",
    parent_joint="upperarm",
    children=["wrist"],
    control=Control(
        name="lowerarm",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="clavicle",
    )
)

wrist = Segment(
    name="wrist",
    translateX=25,
    translateY=0,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="arm",
    parent_joint="lowerarm",
    children=[""],
    control=Control(
        name="wrist",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="lowerarm",
    )
)

arm_module = Module(
    name="arm",
    component_type="arm",
    children=[""],
    segments=[clavicle, upperarm, lowerarm, wrist],
    parent_node=None,
    parent_joint=None,
    mirror=True,
    stretch=True,
    twist=True,
    twist_joints=5,
    twist_influence=0.5
)
