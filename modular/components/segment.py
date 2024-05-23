from dataclasses import dataclass

from utilities.enums import Orient
from typing import Optional

from modular.components.control import Control


@dataclass
class Segment:
    name: str
    parent: Optional["Segment"]
    position: tuple[float, float, float]
    orientation: Orient
    control: Control
