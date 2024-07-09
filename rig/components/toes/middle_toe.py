from rig.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

middle_toe_meta_control = Control(name="middle_toe_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
middle_toe_meta_joint = Segment(name="middle_toe_meta", parent=None, position=(-1, 2, 0),
                                orientation=Orient.BONE,
                                control=middle_toe_meta_control)

middle_toe_01_control = Control(name="middle_toe_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
middle_toe_01_joint = Segment(name="middle_toe_01", parent=middle_toe_meta_joint, position=(0, -2, 2),
                              orientation=Orient.BONE,
                              control=middle_toe_01_control)

middle_toe_02_control = Control(name="middle_toe_02", parent=middle_toe_01_control, shape=Shape.CUBE, color=Color.GREEN,
                                scale=1)
middle_toe_02_joint = Segment(name="middle_toe_02", parent=middle_toe_01_joint, position=(0, 0, 3),
                              orientation=Orient.BONE,
                              control=middle_toe_02_control)

middle_toe_03_control = Control(name="middle_toe_03", parent=middle_toe_02_control, shape=Shape.CUBE, color=Color.GREEN,
                                scale=1)
middle_toe_03_joint = Segment(name="middle_toe_03", parent=middle_toe_02_joint, position=(0, -0.5, 2),
                              orientation=Orient.WORLD,
                              control=middle_toe_03_control)

middle_toe_segments: list[Segment] = [middle_toe_meta_joint, middle_toe_01_joint, middle_toe_02_joint,
                                      middle_toe_03_joint]
