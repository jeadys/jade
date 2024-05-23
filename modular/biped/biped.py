from enum import Enum
from abc import ABC, abstractmethod
from dataclasses import dataclass

from utilities.enums import Orient, Shape, Color
from typing import Optional


@dataclass
class Control:
    name: str
    shape: Shape
    color: Color
    scale: float
    parent: Optional["Control"]
    generate: bool = True


@dataclass
class Segment:
    name: str
    parent: Optional["Segment"]
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
