import json
from dataclasses import asdict, dataclass, field
from typing import Literal

from jade.enums import Orient, RotateOrder


@dataclass
class Control:
    name: str
    parent_control: str | None
    control_points: list[list[float | int]] | None = field(default_factory=lambda: [[0.0, 0.0, 0.0, 1.0]])
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
class Twist:
    enabled: bool
    twist_joints: int
    twist_influence: float

    @classmethod
    def from_dict(cls, data: dict | None):
        return cls(**data)


@dataclass
class Stretch:
    enabled: bool
    stretchiness: float
    stretch_volume: float
    stretch_type: int

    @classmethod
    def from_dict(cls, data: dict | None):
        return cls(**data)


@dataclass
class Ribbon:
    enabled: bool
    divisions: int
    width: float
    length: float
    ribbon_controls: int
    tweak_controls: int

    @classmethod
    def from_dict(cls, data: dict | None):
        return cls(**data)


@dataclass
class Module:
    name: str
    module_type: str
    children: list[str] | None
    segments: list[Segment]
    parent_node: str | None
    parent_joint: str | None
    module_nr: str | None = None
    side: Literal["L_", "R_"] = ""
    twist: Twist | None = None
    stretch: Stretch | None = None
    ribbon: Ribbon | None = None

    @classmethod
    def from_dict(cls, data: dict):
        segments_data = data.pop("segments", [])
        segments = [Segment.from_dict(segment_data) for segment_data in segments_data]
        twist_data = data.pop("twist", None)
        stretch_data = data.pop("stretch", None)
        ribbon_data = data.pop("ribbon", None)

        twist = Twist.from_dict(twist_data) if twist_data else None
        stretch = Stretch.from_dict(stretch_data) if stretch_data else None
        ribbon = Ribbon.from_dict(ribbon_data) if ribbon_data else None

        return cls(
            segments=segments,
            twist=twist,
            stretch=stretch,
            ribbon=ribbon,
            **data
        )


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
