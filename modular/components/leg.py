from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color


def leg_segments() -> list[Segment]:
    upperleg_control = Control(name="upperleg", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    upperleg_joint = Segment(name="upperleg", parent=None, position=(10, 90, 0), orientation=Orient.BONE,
                             control=upperleg_control)

    lowerleg_control = Control(name="lowerleg", parent=upperleg_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    lowerleg_joint = Segment(name="lowerleg", parent=upperleg_joint, position=(0, -40, 0), orientation=Orient.BONE,
                             control=lowerleg_control)

    ankle_control = Control(name="ankle", parent=lowerleg_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    ankle_joint = Segment(name="ankle", parent=lowerleg_joint, position=(0, -40, -7.5), orientation=Orient.SKIP,
                          control=ankle_control)

    ball_control = Control(name="ball", parent=ankle_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    ball_joint = Segment(name="ball", parent=ankle_joint, position=(0, -10, 7.5), orientation=Orient.BONE,
                         control=ball_control)

    toe_control = Control(name="toe", parent=ball_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    toe_joint = Segment(name="toe", parent=ball_joint, position=(0, 0, 7.5), orientation=Orient.WORLD,
                        control=toe_control)

    return [upperleg_joint, lowerleg_joint, ankle_joint, ball_joint, toe_joint]
