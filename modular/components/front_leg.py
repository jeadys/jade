from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color


def front_leg_segments() -> list[Segment]:
    front_clavicle_control = Control(name="front_clavicle", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    front_clavicle_joint = Segment(name="front_clavicle", parent=None, position=(5, 50, 15), orientation=Orient.BONE,
                                   control=front_clavicle_control)

    front_upperarm_control = Control(name="front_upperarm", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
    front_upperarm_joint = Segment(name="front_upperarm", parent=front_clavicle_joint, position=(0, -10, 7.5),
                                   orientation=Orient.BONE, control=front_upperarm_control)

    front_lowerarm_control = Control(name="front_lowerarm", parent=front_upperarm_control, shape=Shape.CUBE,
                                     color=Color.GREEN, scale=5)
    front_lowerarm_joint = Segment(name="front_lowerarm", parent=front_upperarm_joint, position=(0, -10, -7.5),
                                   orientation=Orient.BONE, control=front_lowerarm_control)

    front_wrist_control = Control(name="front_wrist", parent=front_lowerarm_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=5)
    front_wrist_joint = Segment(name="front_wrist", parent=front_lowerarm_joint, position=(0, -20, 2.5),
                                orientation=Orient.BONE, control=front_wrist_control)

    front_paw_control = Control(name="front_paw", parent=front_wrist_control, shape=Shape.CUBE, color=Color.GREEN,
                                scale=5)
    front_paw_joint = Segment(name="front_paw", parent=front_wrist_joint, position=(0, -10, 2.5),
                              orientation=Orient.SKIP, control=front_paw_control)

    return [front_clavicle_joint, front_upperarm_joint, front_lowerarm_joint, front_wrist_joint, front_paw_joint]
