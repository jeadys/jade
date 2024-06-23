from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

thumb_finger_meta_control = Control(name="thumb_finger_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
thumb_finger_meta_joint = Segment(name="thumb_finger_meta", parent=None, position=(0, 0, 3),
                                  orientation=Orient.BONE,
                                  control=thumb_finger_meta_control)

thumb_finger_01_control = Control(name="thumb_finger_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
thumb_finger_01_joint = Segment(name="thumb_finger_01", parent=thumb_finger_meta_joint, position=(3, -1, 1),
                                orientation=Orient.BONE,
                                control=thumb_finger_01_control)

thumb_finger_02_control = Control(name="thumb_finger_02", parent=thumb_finger_01_control, shape=Shape.CUBE,
                                  color=Color.GREEN,
                                  scale=1)
thumb_finger_02_joint = Segment(name="thumb_finger_02", parent=thumb_finger_01_joint, position=(2.25, -0.75, 0.375),
                                orientation=Orient.BONE,
                                control=thumb_finger_02_control)

thumb_finger_03_control = Control(name="thumb_finger_03", parent=thumb_finger_02_control, shape=Shape.CUBE,
                                  color=Color.GREEN,
                                  scale=1)
thumb_finger_03_joint = Segment(name="thumb_finger_03", parent=thumb_finger_02_joint, position=(1.5, -0.5, 0.25),
                                orientation=Orient.WORLD,
                                control=thumb_finger_03_control)

thumb_finger_segments: list[Segment] = [thumb_finger_meta_joint, thumb_finger_01_joint, thumb_finger_02_joint,
                                        thumb_finger_03_joint]
