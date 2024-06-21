from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

clavicle_control = Control(name="clavicle", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
clavicle_joint = Segment(name="clavicle", parent=None, position=(5, 140, 5), orientation=Orient.BONE,
                         control=clavicle_control)

upperarm_control = Control(name="upperarm", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
upperarm_joint = Segment(name="upperarm", parent=clavicle_joint, position=(10, 0, -15), orientation=Orient.BONE,
                         control=upperarm_control)

lowerarm_control = Control(name="lowerarm", parent=upperarm_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
lowerarm_joint = Segment(name="lowerarm", parent=upperarm_joint, position=(30, 0, -7.5), orientation=Orient.BONE,
                         control=lowerarm_control)

wrist_control = Control(name="wrist", parent=lowerarm_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
wrist_joint = Segment(name="wrist", parent=lowerarm_joint, position=(25, 0, 0), orientation=Orient.WORLD,
                      control=wrist_control)

arm_segments: list[Segment] = [clavicle_joint, upperarm_joint, lowerarm_joint, wrist_joint]
