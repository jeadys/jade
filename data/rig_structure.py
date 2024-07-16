from utilities.enums import Orient, Color, Shape, RotateOrder
from dataclasses import dataclass, asdict, field
import json
from typing import Literal


@dataclass
class Control:
    name: str
    control_shape: Shape | None
    control_color: Color | None
    control_scale: float | None
    parent_control: str | None
    control_points: list[list[float | int]] | None = field(default_factory=lambda:  [[0.0, 0.0, 0.0, 1.0]])
    control_rgb: list[float | int] | None = field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotateOrder: RotateOrder = RotateOrder.XYZ

    @classmethod
    def from_dict(cls, data: dict | None):
        return cls(**data)


@dataclass
class Segment:
    name: str
    translateX: float
    translateY: float
    translateZ: float
    rotateX: float
    rotateY: float
    rotateZ: float
    scaleX: float
    scaleY: float
    scaleZ: float
    rotateOrder: RotateOrder
    orientation: Orient
    parent_node: str | None
    parent_joint: str | None
    children: list[str]
    control: Control | None

    @classmethod
    def from_dict(cls, data: dict):
        control_data = data.pop("control", None)
        control_instance = Control.from_dict(control_data) if control_data is not None else None
        return cls(control=control_instance, **data)


@dataclass
class Module:
    name: str
    module_type: str
    children: list[str] | None
    segments: list[Segment]
    parent_node: str | None
    parent_joint: str | None
    mirror: bool
    stretch: bool
    twist: float
    twist_joints: int
    twist_influence: float
    module_nr: str | None = None
    side: Literal["L_", "R_"] = ""

    @classmethod
    def from_dict(cls, data: dict):
        segments_data = data.pop("segments", [])
        segments = [Segment.from_dict(segment_data) for segment_data in segments_data]
        return cls(segments=segments, **data)


@dataclass
class Rig:
    name: str
    description: str
    modules: dict[str, Module]

    @classmethod
    def from_dict(cls, data: dict):
        modules_data = data.get("modules", {})
        modules = {module_name: Module.from_dict(module_data) for module_name, module_data in modules_data.items()}
        return cls(name=data.get("name"), description=data.get("description"), modules=modules)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class Twist:
    add_twist: bool
    twist_joints: int
    twist_influence: float


@dataclass
class Stretch:
    add_stretch: bool
    stretchiness: float
    stretch_volume: float
    stretch_type: int
