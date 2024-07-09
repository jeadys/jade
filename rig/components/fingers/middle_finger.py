from rig.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

middle_finger_meta_control = Control(name="middle_finger_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN,
                                     scale=1)
middle_finger_meta_joint = Segment(name="middle_finger_meta", parent=None, position=(0, 0, 0),
                                   orientation=Orient.BONE,
                                   control=middle_finger_meta_control)

middle_finger_01_control = Control(name="middle_finger_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
middle_finger_01_joint = Segment(name="middle_finger_01", parent=middle_finger_meta_joint, position=(5, 0, 0),
                                 orientation=Orient.BONE,
                                 control=middle_finger_01_control)

middle_finger_02_control = Control(name="middle_finger_02", parent=middle_finger_01_control, shape=Shape.CUBE,
                                   color=Color.GREEN,
                                   scale=1)
middle_finger_02_joint = Segment(name="middle_finger_02", parent=middle_finger_01_joint, position=(3.5, -0.15, 0),
                                 orientation=Orient.BONE,
                                 control=middle_finger_02_control)

middle_finger_03_control = Control(name="middle_finger_03", parent=middle_finger_02_control, shape=Shape.CUBE,
                                   color=Color.GREEN,
                                   scale=1)
middle_finger_03_joint = Segment(name="middle_finger_03", parent=middle_finger_02_joint, position=(2, -0.45, 0),
                                 orientation=Orient.BONE,
                                 control=middle_finger_03_control)

middle_finger_04_control = Control(name="middle_finger_04", parent=middle_finger_03_control, shape=Shape.CUBE,
                                   color=Color.GREEN,
                                   scale=1)
middle_finger_04_joint = Segment(name="middle_finger_04", parent=middle_finger_03_joint, position=(1, -0.45, 0),
                                 orientation=Orient.WORLD,
                                 control=middle_finger_04_control)

middle_finger_segments: list[Segment] = [middle_finger_meta_joint, middle_finger_01_joint, middle_finger_02_joint,
                                         middle_finger_03_joint, middle_finger_04_joint]
