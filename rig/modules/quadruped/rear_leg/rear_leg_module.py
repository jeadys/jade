from data.rig_structure import Control, Module, Segment
from utilities.enums import Color, Orient, RotateOrder, Shape

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
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
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
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
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
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
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
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
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
        control_shape=Shape.CUBE,
        control_color=Color.GREEN,
        control_scale=5,
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
    mirror=True,
    stretch=True,
    twist=True,
    twist_joints=5,
    twist_influence=0.5
)
