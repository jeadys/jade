from utilities.enums import Orient, Color, Shape, RotateOrder
from dataclasses import dataclass, asdict
import json


@dataclass
class Control:
    name: str
    control_shape: Shape | None
    control_color: Color | None
    control_scale: float | None
    parent_control: str | None
    rotateOrder: RotateOrder = RotateOrder.XYZ

    @classmethod
    def from_dict(cls, data: dict):
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
    control: Control

    @classmethod
    def from_dict(cls, data: dict):
        control_data = data.pop("control", {})
        return cls(control=Control.from_dict(control_data), **data)


@dataclass
class Module:
    name: str
    component_type: str
    children: list[str] | None
    segments: list[Segment]
    parent_node: str | None
    parent_joint: str | None
    mirror: bool
    stretch: bool
    twist: float
    twist_joints: int
    twist_influence: float

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
