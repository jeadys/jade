from data.rig_structure import Control, Module, Segment, Twist, Ribbon, Stretch
from utilities.enums import Color, Orient, RotateOrder, Shape, StretchMode
from utilities.shapes import cube_points

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
        parent_control=None,
        control_points=cube_points,
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
        parent_control=None,
        control_points=cube_points,

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
        parent_control="upperarm",
        control_points=cube_points,
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
        parent_control="lowerarm",
        control_points=cube_points,
    )
)

arm_module = Module(
    name="arm",
    module_type="arm",
    children=[""],
    segments=[clavicle, upperarm, lowerarm, wrist],
    parent_node=None,
    parent_joint=None,
    twist=Twist(
        enabled=True,
        twist_joints=2,
        twist_influence=0.5
    ),
    stretch=Stretch(
        enabled=True,
        stretch_type=StretchMode.STRETCH,
        stretchiness=1,
        stretch_volume=0.5,
    ),
    ribbon=Ribbon(
        enabled=False,
        divisions=8,
        width=50,
        length=0.1,
        ribbon_controls=1,
        tweak_controls=2
    )
)
