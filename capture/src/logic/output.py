from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field, fields

from logic.marker import Marker

class TypeScriptSerializable(ABC):
    @abstractmethod
    def to_typescript(self) -> str:
        pass

def indent(code: str) -> str:
    return "\n".join([f"    {line}" for line in code.splitlines()])

class TypeScriptSerializableDataclass(TypeScriptSerializable):
    def to_typescript(self) -> str:
        field_values = ((field.name, getattr(self, field.name)) for field in fields(self))
        rendered_fields = ((k, v.to_typescript()) for k, v in field_values if v is not None)

        code = ",\n".join(f"{k}: {v.to_typescript()}" for k, v in rendered_fields if v)

        if code:
            return f"{{\n{indent(code)}\n}}"
        else:
            return ""

@dataclass
class Vector3(TypeScriptSerializable):
    x: float
    y: float
    z: float

    def to_typescript(self) -> str:
        return f"new Vector3({self.x}, {self.y}, {self.z})"

@dataclass
class ElementPos(TypeScriptSerializableDataclass):
    neutralPos: Vector3
    normal: Vector3
    down: Vector3

@dataclass
class FingerPositionOptions(TypeScriptSerializableDataclass):
    pinky: ElementPos | None = None
    ringFinger: ElementPos | None = None
    middleFinger: ElementPos | None = None
    indexFinger: ElementPos | None = None
    thumb: ElementPos | None = None
    resetButton: ElementPos | None = None

@dataclass
class SocketPositionOptions(TypeScriptSerializableDataclass):
    topSocket: ElementPos | None = None
    bottomSocket: ElementPos | None = None

@dataclass
class PositionOptions(TypeScriptSerializableDataclass):
    plate: ElementPos | None = None
    socket: SocketPositionOptions = field(default_factory=SocketPositionOptions)
    finger: FingerPositionOptions = field(default_factory=FingerPositionOptions)

    def set_position(self, marker: Marker, pos: ElementPos | None):
        match marker:
            case Marker.PLATE:
                self.plate = pos
            case Marker.TOP_SOCKET:
                self.socket.topSocket = pos
            case Marker.BOTTOM_SOCKET:
                self.socket.bottomSocket = pos
            case Marker.PINKY:
                self.finger.pinky = pos
            case Marker.RING_FINGER:
                self.finger.ringFinger = pos
            case Marker.MIDDLE_FINGER:
                self.finger.middleFinger = pos
            case Marker.INDEX_FINGER:
                self.finger.indexFinger = pos
            case Marker.THUMB:
                self.finger.thumb = pos
            case Marker.RESET_BUTTON:
                self.finger.resetButton = pos

    def export(self, file_name: str):
        with open(file_name, "w") as file:
            obj = self.to_typescript() or "{}"
            code = f"{obj} as const satisfies DeepPartial<PositionOptions, ElementPos>"
            file.write(code)
