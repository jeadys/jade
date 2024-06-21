from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

wing_humerus_control = Control(name="wing_humerus", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=2.5)
wing_humerus_joint = Segment(name="wing_humerus", parent=None, position=(0, 0, 0), orientation=Orient.BONE,
                             control=wing_humerus_control)

wing_ulna_control = Control(name="wing_ulna", parent=wing_humerus_control, shape=Shape.CUBE, color=Color.GREEN,
                            scale=2.5)
wing_ulna_joint = Segment(name="wing_ulna", parent=wing_humerus_joint, position=(10, 0, 10),
                          orientation=Orient.BONE,
                          control=wing_ulna_control)

wing_manus_control = Control(name="wing_manus", parent=wing_ulna_control, shape=Shape.CUBE, color=Color.GREEN,
                             scale=2.5)
wing_manus_joint = Segment(name="wing_manus", parent=wing_ulna_joint, position=(10, 0, 2.5),
                           orientation=Orient.BONE,
                           control=wing_manus_control)

wing_phalanx_control = Control(name="wing_phalanx", parent=wing_manus_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=2.5)
wing_phalanx_joint = Segment(name="wing_phalanx", parent=wing_manus_joint, position=(10, 0, -2.5),
                             orientation=Orient.BONE, control=wing_phalanx_control)

wing_ulna_01_control = Control(name="wing_ulna_01", parent=wing_ulna_control, shape=Shape.CUBE, color=Color.GREEN,
                               scale=2.5)
wing_ulna_01_joint = Segment(name="wing_ulna_01", parent=wing_ulna_joint, position=(2.5, 0, -5),
                             orientation=Orient.BONE, control=wing_ulna_01_control)
wing_ulna_02_control = Control(name="wing_ulna_02", parent=wing_ulna_01_control, shape=Shape.CUBE,
                               color=Color.GREEN,
                               scale=2.5)
wing_ulna_02_joint = Segment(name="wing_ulna_02", parent=wing_ulna_01_joint, position=(2.5, 0, -5),
                             orientation=Orient.WORLD, control=wing_ulna_02_control)

wing_manus_01_control = Control(name="wing_manus_01", parent=wing_manus_control, shape=Shape.CUBE,
                                color=Color.GREEN,
                                scale=2.5)
wing_manus_01_joint = Segment(name="wing_manus_01", parent=wing_manus_joint, position=(2.5, 0, -5),
                              orientation=Orient.BONE, control=wing_manus_01_control)
wing_manus_02_control = Control(name="wing_manus_02", parent=wing_manus_01_control, shape=Shape.CUBE,
                                color=Color.GREEN,
                                scale=2.5)
wing_manus_02_joint = Segment(name="wing_manus_02", parent=wing_manus_01_joint, position=(2.5, 0, -5),
                              orientation=Orient.WORLD, control=wing_manus_02_control)

wing_phalanx_01_control = Control(name="wing_phalanx_01", parent=wing_phalanx_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=2.5)
wing_phalanx_01_joint = Segment(name="wing_phalanx_01", parent=wing_phalanx_joint, position=(5, 0, -5),
                                orientation=Orient.BONE, control=wing_phalanx_01_control)
wing_phalanx_02_control = Control(name="wing_phalanx_02", parent=wing_phalanx_01_control, shape=Shape.CUBE,
                                  color=Color.GREEN, scale=2.5)
wing_phalanx_02_joint = Segment(name="wing_phalanx_02", parent=wing_phalanx_01_joint, position=(5, 0, -5),
                                orientation=Orient.WORLD, control=wing_phalanx_02_control)

wing_segments: list[Segment] = [wing_humerus_joint, wing_ulna_joint, wing_manus_joint, wing_phalanx_joint,
                                wing_phalanx_01_joint, wing_phalanx_02_joint, wing_manus_01_joint, wing_manus_02_joint,
                                wing_ulna_01_joint, wing_ulna_02_joint]
