from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, fields
import os

OUT_DIR = "out"

class TypeScriptSerializable(ABC):
    @abstractmethod
    def to_typescript(self) -> str:
        pass

def indent(code: str) -> str:
    return "\n".join([f"    {line}" for line in code.splitlines()])

class TypeScriptSerializableDataclass(TypeScriptSerializable):
    def to_typescript(self) -> str:
        fields = ((field.name, getattr(self, field.name)) for field in fields(self))
        rendered_fields = ((k, v.to_typescript()) for k, v in fields if v is not None)

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
    pinky: ElementPos | None
    ringFinger: ElementPos | None
    middleFinger: ElementPos | None
    indexFinger: ElementPos | None
    thumb: ElementPos | None
    resetButton: ElementPos | None

@dataclass
class SocketPositionOptions(TypeScriptSerializableDataclass):
    topSocket: ElementPos | None
    bottomSocket: ElementPos | None

@dataclass
class PositionOptions(TypeScriptSerializableDataclass):
    plate: ElementPos | None
    socket: SocketPositionOptions | None
    finger: FingerPositionOptions | None

    def export(self, name: str):
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        with open(os.path.join(OUT_DIR, f"{name}.ts.txt"), "w") as file:
            obj = self.to_typescript() or "{}"
            code = f"{obj} as const satisfies DeepPartial<PositionOptions, ElementPos>"
            file.write(code)
