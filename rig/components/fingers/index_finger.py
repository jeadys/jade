from rig.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

index_finger_meta_control = Control(name="index_finger_meta", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
index_finger_meta_joint = Segment(name="index_finger_meta", parent=None, position=(0, 0, 1.5),
                                  orientation=Orient.BONE, control=index_finger_meta_control)

index_finger_01_control = Control(name="index_finger_01", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=1)
index_finger_01_joint = Segment(name="index_finger_01", parent=index_finger_meta_joint, position=(5, 0, 0),
                                orientation=Orient.BONE, control=index_finger_01_control)

index_finger_02_control = Control(name="index_finger_02", parent=index_finger_01_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=1)
index_finger_02_joint = Segment(name="index_finger_02", parent=index_finger_01_joint, position=(3, -0.10, 0),
                                orientation=Orient.BONE, control=index_finger_02_control)

index_finger_03_control = Control(name="index_finger_03", parent=index_finger_02_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=1)
index_finger_03_joint = Segment(name="index_finger_03", parent=index_finger_02_joint, position=(2, -0.35, 0),
                                orientation=Orient.BONE, control=index_finger_03_control)

index_finger_04_control = Control(name="index_finger_04", parent=index_finger_03_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=1)
index_finger_04_joint = Segment(name="index_finger_04", parent=index_finger_03_joint, position=(1, -0.35, 0),
                                orientation=Orient.WORLD, control=index_finger_04_control)

index_finger_segments: list[Segment] = [index_finger_meta_joint, index_finger_01_joint, index_finger_02_joint,
                                        index_finger_03_joint, index_finger_04_joint]
