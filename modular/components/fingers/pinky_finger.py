from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

pinky_finger_meta_control = Control(name="pinky_finger_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
pinky_finger_meta_joint = Segment(name="pinky_finger_meta", parent=None, position=(0, 0, -3),
                                  orientation=Orient.BONE,
                                  control=pinky_finger_meta_control)

pinky_finger_01_control = Control(name="pinky_finger_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
pinky_finger_01_joint = Segment(name="pinky_finger_01", parent=pinky_finger_meta_joint, position=(3, 0, 0),
                                orientation=Orient.BONE,
                                control=pinky_finger_01_control)

pinky_finger_02_control = Control(name="pinky_finger_02", parent=pinky_finger_01_control, shape=Shape.CUBE,
                                  color=Color.GREEN,
                                  scale=1)
pinky_finger_02_joint = Segment(name="pinky_finger_02", parent=pinky_finger_01_joint, position=(2.5, -0.5, 0),
                                orientation=Orient.BONE,
                                control=pinky_finger_02_control)

pinky_finger_03_control = Control(name="pinky_finger_03", parent=pinky_finger_02_control, shape=Shape.CUBE,
                                  color=Color.GREEN,
                                  scale=1)
pinky_finger_03_joint = Segment(name="pinky_finger_03", parent=pinky_finger_02_joint, position=(1.5, -0.5, 0),
                                orientation=Orient.BONE,
                                control=pinky_finger_03_control)

pinky_finger_04_control = Control(name="pinky_finger_04", parent=pinky_finger_03_control, shape=Shape.CUBE,
                                  color=Color.GREEN,
                                  scale=1)
pinky_finger_04_joint = Segment(name="pinky_finger_04", parent=pinky_finger_03_joint, position=(1, -0.5, 0),
                                orientation=Orient.WORLD,
                                control=pinky_finger_04_control)

pinky_finger_segments: list[Segment] = [pinky_finger_meta_joint, pinky_finger_01_joint, pinky_finger_02_joint,
                                        pinky_finger_03_joint, pinky_finger_04_joint]
