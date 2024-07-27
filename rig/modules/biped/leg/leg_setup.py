from data.rig_structure import Control, Module, Ribbon, Segment, Stretch, Twist
from utilities.enums import Orient, RotateOrder, StretchMode
from utilities.shapes import cube_points

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
        parent_control=None,
        control_points=cube_points,
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
        parent_control="upperleg",
        control_points=cube_points,
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
        parent_control="lowerleg",
        control_points=cube_points,
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
        parent_control="ankle",
        control_points=cube_points,
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
        parent_control="ball",
        control_points=cube_points,
    )
)

leg_module = Module(
    name="leg",
    module_type="leg",
    children=[""],
    segments=[upperleg, lowerleg, ankle, ball, toe],
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
