from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

ring_toe_meta_control = Control(name="ring_toe_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
ring_toe_meta_joint = Segment(name="ring_toe_meta", parent=None, position=(1, 2, 0),
                              orientation=Orient.BONE,
                              control=ring_toe_meta_control)

ring_toe_01_control = Control(name="ring_toe_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
ring_toe_01_joint = Segment(name="ring_toe_01", parent=ring_toe_meta_joint, position=(0, -2, 2),
                            orientation=Orient.BONE,
                            control=ring_toe_01_control)

ring_toe_02_control = Control(name="ring_toe_02", parent=ring_toe_01_control, shape=Shape.CUBE, color=Color.GREEN,
                              scale=1)
ring_toe_02_joint = Segment(name="ring_toe_02", parent=ring_toe_01_joint, position=(0, 0, 3),
                            orientation=Orient.BONE,
                            control=ring_toe_02_control)

ring_toe_03_control = Control(name="ring_toe_03", parent=ring_toe_02_control, shape=Shape.CUBE, color=Color.GREEN,
                              scale=1)
ring_toe_03_joint = Segment(name="ring_toe_03", parent=ring_toe_02_joint, position=(0, -0.5, 2),
                            orientation=Orient.WORLD,
                            control=ring_toe_03_control)

ring_toe_segments: list[Segment] = [ring_toe_meta_joint, ring_toe_01_joint, ring_toe_02_joint, ring_toe_03_joint]
