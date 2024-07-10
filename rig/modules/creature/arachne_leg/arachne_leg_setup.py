from data.rig_structure import Control, Module, Segment
from utilities.enums import Color, Orient, RotateOrder, Shape

arachne_thigh = Segment(
    name="arachne_thigh",
    translateX=5,
    translateY=10,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arachne_leg",
    parent_joint=None,
    children=["arachne_shin"],
    control=Control(
        name="arachne_thigh",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control=None,
    )
)

arachne_shin = Segment(
    name="arachne_shin",
    translateX=10,
    translateY=5,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arachne_leg",
    parent_joint="arachne_thigh",
    children=["arachne_foot"],
    control=Control(
        name="arachne_shin",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control="arachne_thigh",
    )
)

arachne_foot = Segment(
    name="arachne_foot",
    translateX=2.5,
    translateY=-10,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="arachne_leg",
    parent_joint="arachne_shin",
    children=["arachne_toe"],
    control=Control(
        name="arachne_foot",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control="arachne_shin",
    )
)

arachne_toe = Segment(
    name="arachne_toe",
    translateX=0,
    translateY=-5,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="arachne_leg",
    parent_joint="arachne_foot",
    children=[""],
    control=Control(
        name="arachne_toe",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=2.5,
        parent_control="arachne_foot",
    )
)


arachne_leg_module = Module(
    name="arachne_leg",
    module_type="arachne_leg",
    children=[""],
    segments=[arachne_thigh, arachne_shin, arachne_foot, arachne_toe],
    parent_node=None,
    parent_joint=None,
    mirror=True,
    stretch=True,
    twist=True,
    twist_joints=5,
    twist_influence=0.5
)
