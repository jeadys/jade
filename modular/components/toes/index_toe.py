from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

index_toe_meta_control = Control(name="index_toe_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
index_toe_meta_joint = Segment(name="index_toe_meta", parent=None, position=(-2, 2, 0),
                               orientation=Orient.BONE,
                               control=index_toe_meta_control)

index_toe_01_control = Control(name="index_toe_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
index_toe_01_joint = Segment(name="index_toe_01", parent=index_toe_meta_joint, position=(0, -2, 2),
                             orientation=Orient.BONE,
                             control=index_toe_01_control)

index_toe_02_control = Control(name="index_toe_02", parent=index_toe_01_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=1)
index_toe_02_joint = Segment(name="index_toe_02", parent=index_toe_01_joint, position=(0, 0, 3),
                             orientation=Orient.BONE,
                             control=index_toe_02_control)

index_toe_03_control = Control(name="index_toe_03", parent=index_toe_02_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=1)
index_toe_03_joint = Segment(name="index_toe_03", parent=index_toe_02_joint, position=(0, -0.5, 2),
                             orientation=Orient.WORLD,
                             control=index_toe_03_control)

index_toe_segments: list[Segment] = [index_toe_meta_joint, index_toe_01_joint, index_toe_02_joint, index_toe_03_joint]
