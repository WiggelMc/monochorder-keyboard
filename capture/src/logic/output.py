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
        code = ",\n".join([f"{field.name}: {getattr(self, field.name).to_typescript()}" for field in fields(self)])
        return f"{{\n{indent(code)}\n}}"

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
    pressedPos: Vector3
    lowerPos: Vector3

@dataclass
class FingerPositionOptions(TypeScriptSerializableDataclass):
    pinky: ElementPos
    ringFinger: ElementPos
    middleFinger: ElementPos
    indexFinger: ElementPos
    thumb: ElementPos
    resetButton: ElementPos

@dataclass
class SocketPositionOptions(TypeScriptSerializableDataclass):
    topSocket: ElementPos
    bottomSocket: ElementPos

@dataclass
class PositionOptions(TypeScriptSerializableDataclass):
    plate: ElementPos
    socket: SocketPositionOptions
    finger: FingerPositionOptions

    def export(self, name: str):
        if not os.path.exists(OUT_DIR):
            os.makedirs(OUT_DIR)

        with open(os.path.join(OUT_DIR, f"{name}.ts.txt"), "w") as file:
            file.write(self.to_typescript())
