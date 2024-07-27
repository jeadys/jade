from data.rig_structure import Control, Module, Ribbon, Segment, Stretch, Twist
from utilities.enums import Orient, RotateOrder, StretchMode

rear_hip = Segment(
    name="rear_hip",
    translateX=5,
    translateY=40,
    translateZ=-25,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="rear_leg",
    parent_joint=None,
    children=["rear_knee"],
    control=Control(
        name="rear_hip",
        parent_control=None,
    )
)

rear_knee = Segment(
    name="rear_knee",
    translateX=0,
    translateY=-15,
    translateZ=2.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="rear_leg",
    parent_joint="rear_hip",
    children=["rear_heel"],
    control=Control(
        name="rear_knee",
        parent_control="rear_hip",
    )
)

rear_heel = Segment(
    name="rear_heel",
    translateX=0,
    translateY=-10,
    translateZ=-12.5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.BONE,
    parent_node="rear_leg",
    parent_joint="rear_knee",
    children=["rear_foot"],
    control=Control(
        name="rear_heel",
        parent_control="rear_knee",
    )
)

rear_foot = Segment(
    name="rear_foot",
    translateX=0,
    translateY=-10,
    translateZ=0,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.WORLD,
    parent_node="rear_leg",
    parent_joint="rear_heel",
    children=["rear_toe"],
    control=Control(
        name="rear_foot",
        parent_control="rear_heel",
    )
)

rear_toe = Segment(
    name="rear_toe",
    translateX=0,
    translateY=-5,
    translateZ=5,
    rotateX=0,
    rotateY=0,
    rotateZ=0,
    scaleX=1,
    scaleY=1,
    scaleZ=1,
    rotateOrder=RotateOrder.XYZ,
    orientation=Orient.SKIP,
    parent_node="rear_leg",
    parent_joint="rear_foot",
    children=[""],
    control=Control(
        name="rear_toe",
        parent_control="rear_foot",
    )
)

rear_leg_module = Module(
    name="rear_leg",
    module_type="rear_leg",
    children=[""],
    segments=[rear_hip, rear_knee, rear_heel, rear_foot, rear_toe],
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
