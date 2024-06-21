from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

arachne_thigh_control = Control(name="arachne_thigh", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=2.5)
arachne_thigh_joint = Segment(name="arachne_thigh", parent=None, position=(5, 10, 0), orientation=Orient.BONE,
                              control=arachne_thigh_control)

arachne_shin_control = Control(name="arachne_shin", parent=arachne_thigh_control, shape=Shape.CUBE,
                               color=Color.GREEN, scale=2.5)
arachne_shin_joint = Segment(name="arachne_shin", parent=arachne_thigh_joint, position=(10, 5, 0),
                             orientation=Orient.BONE, control=arachne_shin_control)

arachne_foot_control = Control(name="arachne_foot", parent=arachne_shin_control, shape=Shape.CUBE,
                               color=Color.GREEN, scale=2.5)
arachne_foot_joint = Segment(name="arachne_foot", parent=arachne_shin_joint, position=(2.5, -10, 0),
                             orientation=Orient.BONE, control=arachne_foot_control)

arachne_toe_control = Control(name="arachne_toe", parent=arachne_foot_control, shape=Shape.CUBE, color=Color.GREEN,
                              scale=2.5)
arachne_toe_joint = Segment(name="arachne_toe", parent=arachne_foot_joint, position=(0, -5, 0),
                            orientation=Orient.WORLD, control=arachne_toe_control)

arachne_leg_segments: list[Segment] = [arachne_thigh_joint, arachne_shin_joint, arachne_foot_joint, arachne_toe_joint]
