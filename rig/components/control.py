from dataclasses import dataclass

from utilities.enums import Shape, Color
from typing import Optional


@dataclass
class Control:
    name: str
    shape: Shape
    color: Color
    scale: float
    parent: Optional["Control"]
    generate: bool = True
