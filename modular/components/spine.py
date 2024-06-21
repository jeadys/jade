from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

spine_01_control = Control(name="spine_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
spine_01_joint = Segment(name="spine_01", parent=None, position=(0, 100, 0), orientation=Orient.BONE,
                         control=spine_01_control)

spine_02_control = Control(name="spine_02", parent=spine_01_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
spine_02_joint = Segment(name="spine_02", parent=spine_01_joint, position=(0, 10, 0), orientation=Orient.BONE,
                         control=spine_02_control)

spine_03_control = Control(name="spine_03", parent=spine_02_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
spine_03_joint = Segment(name="spine_03", parent=spine_02_joint, position=(0, 10, 0), orientation=Orient.BONE,
                         control=spine_03_control)

spine_04_control = Control(name="spine_04", parent=spine_03_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
spine_04_joint = Segment(name="spine_04", parent=spine_03_joint, position=(0, 10, 0), orientation=Orient.BONE,
                         control=spine_04_control)

spine_05_control = Control(name="spine_05", parent=spine_04_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
spine_05_joint = Segment(name="spine_05", parent=spine_04_joint, position=(0, 10, 0), orientation=Orient.BONE,
                         control=spine_05_control)

spine_segments: list[Segment] = [spine_01_joint, spine_02_joint, spine_03_joint, spine_04_joint, spine_05_joint]
