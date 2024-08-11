from enum import Enum


class CustomEnum(Enum):
    def __str__(self):
        return str(self.value)


class RotateOrder(int, Enum):
    XYZ = 0
    YZX = 1
    ZXY = 2
    XZY = 3
    YXZ = 4
    ZYX = 5

    def __int__(self) -> int:
        return int.__int__(self)

    @classmethod
    def enum_to_string_attribute(cls):
        enums = ':'.join([f"{x.name}={x.value}" for x in cls])
        return enums


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


class StretchMode(int, Enum):
    BOTH = 1
    STRETCH = 3
    SQUASH = 5

    def __int__(self) -> int:
        return int.__int__(self)

    @classmethod
    def enum_to_string_attribute(cls):
        enums = ':'.join([f"{x.name}={x.value}" for x in cls])
        return enums


class Mirror(int, Enum):
    NO = 0
    YES = 1

    def __int__(self) -> int:
        return int.__int__(self)


class Layer(int, Enum):
    NO = 0
    YES = 1

    def __int__(self) -> int:
        return int.__int__(self)


class Orient(int, Enum):
    SKIP = 0
    WORLD = 1
    BONE = 2

    def __int__(self) -> int:
        return int.__int__(self)

    @classmethod
    def enum_to_string_attribute(cls):
        enums = ':'.join([f"{x.name}={x.value}" for x in cls])
        return enums


class Color(int, Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    MAGENTA = 4
    CYAN = 5
    WHITE = 6
    BLACK = 7

    def __int__(self) -> int:
        return int.__int__(self)

    @classmethod
    def enum_to_string_attribute(cls):
        enums = ':'.join([f"{x.name}={x.value}" for x in cls])
        return enums


class Shape(int, Enum):
    CIRCLE = 0
    SQUARE = 1
    CUBE = 2
    TRIANGLE = 3
    ARROW = 4
    PLUS = 5
    MINUS = 6
    FOURWAYARROW = 7
    NONE = 8

    def __int__(self) -> int:
        return int.__int__(self)

    @classmethod
    def enum_to_string_attribute(cls):
        enums = ':'.join([f"{x.name}={x.value}" for x in cls])
        return enums


class Rig(int, Enum):
    DEFAULT = 0
    FK = 1
    IK = 2
    FK_IK = 3
    SP = 4
    FK_SP = 5

    def __int__(self) -> int:
        return int.__int__(self)


class Side(int, Enum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2

    def __int__(self) -> int:
        return int.__int__(self)


class TwistFlow(str, Enum):
    FORWARD = "forward"
    BACKWARD = "backward"

    def __int__(self) -> str:
        return str.__str__(self)


def enum_to_string_attribute(enum):
    enums = ':'.join([f"{x.name}={x.value}" for x in enum])

    return enums


enum_to_string_attribute(Color)
