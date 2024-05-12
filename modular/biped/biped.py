from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

from utilities.enums import Orient, Shape, Color


@dataclass
class Control:
    shape: Shape
    color: Color
    scale: float


@dataclass
class Segment:
    name: str
    parent: str | None
    position: tuple[float, float, float]
    orientation: Orient
    control: Control


class Biped(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def skeleton(self):
        pass

    @abstractmethod
    def forward_kinematic(self):
        pass

    @abstractmethod
    def inverse_kinematic(self):
        pass

    @abstractmethod
    def switch_kinematic(self):
        pass
