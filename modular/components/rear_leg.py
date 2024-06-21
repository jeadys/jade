from modular.biped.biped import Segment, Control
from utilities.enums import Orient, Shape, Color

rear_hip_control = Control(name="rear_hip", parent=None, shape=Shape.CUBE, color=Color.GREEN, scale=5)
rear_hip_joint = Segment(name="rear_hip", parent=None, position=(5, 40, -25), orientation=Orient.BONE,
                         control=rear_hip_control)

rear_knee_control = Control(name="rear_knee", parent=rear_hip_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
rear_knee_joint = Segment(name="rear_knee", parent=rear_hip_joint, position=(0, -15, 2.5), orientation=Orient.BONE,
                          control=rear_knee_control)

rear_heel_control = Control(name="rear_heel", parent=rear_knee_control, shape=Shape.CUBE, color=Color.GREEN,
                            scale=5)
rear_heel_joint = Segment(name="rear_heel", parent=rear_knee_joint, position=(0, -10, -12.5),
                          orientation=Orient.BONE, control=rear_heel_control)

rear_foot_control = Control(name="rear_foot", parent=rear_heel_control, shape=Shape.CUBE, color=Color.GREEN,
                            scale=5)
rear_foot_joint = Segment(name="rear_foot", parent=rear_heel_joint, position=(0, -10, 0), orientation=Orient.WORLD,
                          control=rear_foot_control)

rear_toe_control = Control(name="rear_toe", parent=rear_foot_control, shape=Shape.CUBE, color=Color.GREEN, scale=5)
rear_toe_joint = Segment(name="rear_toe", parent=rear_foot_joint, position=(0, -5, 5), orientation=Orient.SKIP,
                         control=rear_toe_control)

rear_leg_segments: list[Segment] = [rear_hip_joint, rear_knee_joint, rear_heel_joint, rear_foot_joint, rear_toe_joint]
