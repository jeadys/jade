from data.rig_structure import Control, Module, Segment
from utilities.enums import Color, Orient, RotateOrder, Shape

upperleg = Segment(
    name="upperleg",
    translateX=10,
    translateY=90,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="leg",
    parent_joint=None,
    children=["lowerleg"],
    control=Control(
        name="upperleg",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control=None,
    )
)

lowerleg = Segment(
    name="lowerleg",
    translateX=0,
    translateY=-40,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="leg",
    parent_joint="upperleg",
    children=["ankle"],
    control=Control(
        name="lowerleg",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="upperleg",
    )
)

ankle = Segment(
    name="ankle",
    translateX=0,
    translateY=-40,
    translateZ=-7.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="leg",
    parent_joint="lowerleg",
    children=["ball"],
    control=Control(
        name="ankle",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="lowerleg",
    )
)

ball = Segment(
    name="ball",
    translateX=0,
    translateY=-10,
    translateZ=7.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="leg",
    parent_joint="ankle",
    children=["toe"],
    control=Control(
        name="ball",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="ankle",
    )
)

toe = Segment(
    name="toe",
    translateX=0,
    translateY=0,
    translateZ=7.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="leg",
    parent_joint="ball",
    children=[""],
    control=Control(
        name="toe",
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
        parent_control="ball",
    )
)

leg_module = Module(
    name="leg",
    module_type="leg",
    children=[""],
    segments=[upperleg, lowerleg, ankle, ball, toe],
    parent_node=None,
    parent_joint=None,
    mirror=True,
    stretch=True,
    twist=True,
    twist_joints=5,
    twist_influence=0.5
)
