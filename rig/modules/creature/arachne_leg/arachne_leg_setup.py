from data.rig_structure import Control, Module, Ribbon, Segment, Stretch, Twist
from utilities.enums import Orient, RotateOrder, StretchMode

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
    twist=Twist(
        enabled=True,
        twist_joints=5,
        twist_influence=0.5
    ),
    stretch=Stretch(
        enabled=True,
        stretch_type=StretchMode.STRETCH,
        stretchiness=0,
        stretch_volume=0,
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
