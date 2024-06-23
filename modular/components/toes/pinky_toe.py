from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

pinky_toe_meta_control = Control(name="pinky_toe_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
pinky_toe_meta_joint = Segment(name="pinky_toe_meta", parent=None, position=(2, 2, 0),
                               orientation=Orient.BONE,
                               control=pinky_toe_meta_control)

pinky_toe_01_control = Control(name="pinky_toe_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
pinky_toe_01_joint = Segment(name="pinky_toe_01", parent=pinky_toe_meta_joint, position=(0, -2, 2),
                             orientation=Orient.BONE,
                             control=pinky_toe_01_control)

pinky_toe_02_control = Control(name="pinky_toe_02", parent=pinky_toe_01_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=1)
pinky_toe_02_joint = Segment(name="pinky_toe_02", parent=pinky_toe_01_joint, position=(0, 0, 3),
                             orientation=Orient.BONE,
                             control=pinky_toe_02_control)

pinky_toe_03_control = Control(name="pinky_toe_03", parent=pinky_toe_02_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=1)
pinky_toe_03_joint = Segment(name="pinky_toe_03", parent=pinky_toe_02_joint, position=(0, -0.5, 2),
                             orientation=Orient.WORLD,
                             control=pinky_toe_03_control)

pinky_toe_segments: list[Segment] = [pinky_toe_meta_joint, pinky_toe_01_joint, pinky_toe_02_joint, pinky_toe_03_joint]
