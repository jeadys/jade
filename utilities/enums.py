from enum import Enum


class CustomEnum(Enum):
    def __str__(self):
        return str(self.value)


class RotateOrder(CustomEnum):
    XYZ = 0
    YZX = 1
    ZXY = 2
    XZY = 3
    YXZ = 4
    ZYX = 5


# Condition node operation
class CONOperation(CustomEnum):
    EQUAL = 0
    NOT_EQUAL = 1
    GREATER_THAN = 2
    GREATER_OR_EQUAL = 3
    LESS_THAN = 4
    LESS_OR_EQUAL = 5


# Plus minus average node operation
class PMAOperation(CustomEnum):
    NO_OPERATION = 0
    SUM = 1
    SUBTRACT = 2
    AVERAGE = 3


# Multiply divide node operation
class MUDOperation(CustomEnum):
    NO_OPERATION = 0
    MULTIPLY = 1
    DIVIDE = 2
    POWER = 3


class WorldUpType(CustomEnum):
    SCENE_UP = 0
    OBJECT_UP = 1
    OBJECT_UP_START_END = 2
    OBJECT_ROTATION_UP = 3
    OBJECT_ROTATION_UP_START_END = 4
    VECTOR = 5
    VECTOR_START_END = 6
    RELATIVE = 7


class ForwardAxis(CustomEnum):
    POSITIVE_X = 0
    NEGATIVE_X = 1
    POSITIVE_Y = 2
    NEGATIVE_Y = 3
    POSITIVE_Z = 4
    NEGATIVE_Z = 5


class UpAxis(CustomEnum):
    POSITIVE_Y = 0
    NEGATIVE_Y = 1
    CLOSEST_Y = 2
    POSITIVE_Z = 3
    NEGATIVE_Z = 4
    CLOSEST_Z = 5
    POSITIVE_X = 6
    NEGATIVE_X = 7
    CLOSEST_X = 8


class Stretch(Enum):
    BOTH = 1
    STRETCH = 3
    SQUASH = 5
