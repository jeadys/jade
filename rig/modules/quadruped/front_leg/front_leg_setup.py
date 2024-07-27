from data.rig_structure import Control, Module, Ribbon, Segment, Stretch, Twist
from utilities.enums import Orient, RotateOrder, StretchMode

front_clavicle = Segment(
    name="front_clavicle",
    translateX=5,
    translateY=50,
    translateZ=15,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="front_leg",
    parent_joint=None,
    children=["front_upperarm"],
    control=Control(
        name="front_clavicle",
        parent_control=None,
    )
)

front_upperarm = Segment(
    name="front_upperarm",
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
    parent_node="front_leg",
    parent_joint="front_clavicle",
    children=["front_lowerarm"],
    control=Control(
        name="front_upperarm",
        parent_control="front_clavicle",
    )
)

front_lowerarm = Segment(
    name="front_lowerarm",
    translateX=0,
    translateY=-10,
    translateZ=-7.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="front_leg",
    parent_joint="front_upperarm",
    children=["front_wrist"],
    control=Control(
        name="front_lowerarm",
        parent_control="front_upperarm",
    )
)

front_wrist = Segment(
    name="front_wrist",
    translateX=0,
    translateY=-20,
    translateZ=2.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="front_leg",
    parent_joint="front_lowerarm",
    children=["front_paw"],
    control=Control(
        name="front_wrist",
        parent_control="front_lowerarm",
    )
)

front_paw = Segment(
    name="front_paw",
    translateX=0,
    translateY=-10,
    translateZ=2.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.SKIP,
    parent_node="front_leg",
    parent_joint="front_wrist",
    children=[""],
    control=Control(
        name="front_paw",
        parent_control="front_wrist",
    )
)

front_leg_module = Module(
    name="front_leg",
    module_type="front_leg",
    children=[""],
    segments=[front_clavicle, front_upperarm, front_lowerarm, front_wrist, front_paw],
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
