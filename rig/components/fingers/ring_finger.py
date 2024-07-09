from rig.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

ring_finger_meta_control = Control(name="ring_finger_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
ring_finger_meta_joint = Segment(name="ring_finger_meta", parent=None, position=(0, 0, -1.5),
                                 orientation=Orient.BONE,
                                 control=ring_finger_meta_control)

ring_finger_01_control = Control(name="ring_finger_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
ring_finger_01_joint = Segment(name="ring_finger_01", parent=ring_finger_meta_joint, position=(4, 0, 0),
                               orientation=Orient.BONE,
                               control=ring_finger_01_control)

ring_finger_02_control = Control(name="ring_finger_02", parent=ring_finger_01_control, shape=Shape.CUBE,
                                 color=Color.GREEN,
                                 scale=1)
ring_finger_02_joint = Segment(name="ring_finger_02", parent=ring_finger_01_joint, position=(3, -0.25, 0),
                               orientation=Orient.BONE,
                               control=ring_finger_02_control)

ring_finger_03_control = Control(name="ring_finger_03", parent=ring_finger_02_control, shape=Shape.CUBE,
                                 color=Color.GREEN,
                                 scale=1)
ring_finger_03_joint = Segment(name="ring_finger_03", parent=ring_finger_02_joint, position=(2, -0.5, 0),
                               orientation=Orient.BONE,
                               control=ring_finger_03_control)

ring_finger_04_control = Control(name="ring_finger_04", parent=ring_finger_03_control, shape=Shape.CUBE,
                                 color=Color.GREEN,
                                 scale=1)
ring_finger_04_joint = Segment(name="ring_finger_04", parent=ring_finger_03_joint, position=(1, -0.5, 0),
                               orientation=Orient.WORLD,
                               control=ring_finger_04_control)

ring_finger_segments: list[Segment] = [ring_finger_meta_joint, ring_finger_01_joint, ring_finger_02_joint,
                                       ring_finger_03_joint, ring_finger_04_joint]
