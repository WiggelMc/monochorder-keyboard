from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, fields
import os

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

def main():
    options = PositionOptions(
        finger= FingerPositionOptions(
            pinky= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            ringFinger= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            middleFinger= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            indexFinger= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            thumb= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            resetButton= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            )
        ),
        socket=SocketPositionOptions(
            topSocket= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            ),
            bottomSocket= ElementPos(
                neutralPos=Vector3(0,0,0),
                pressedPos=Vector3(0,0,0),
                lowerPos=Vector3(0,0,0)
            )
        ),
        plate= ElementPos(
            neutralPos=Vector3(0,0,0),
            pressedPos=Vector3(0,0,0),
            lowerPos=Vector3(0,0,0)
        )
    )

    out_dir = "out"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(os.path.join(out_dir, "out.ts.txt"), "w") as file:
        file.write(options.to_typescript())

if __name__ == "__main__":
    main()