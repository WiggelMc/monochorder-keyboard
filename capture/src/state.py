from dataclasses import asdict, dataclass, field, fields
from cv2.typing import MatLike
import base64
import json
import numpy as np


@dataclass
class ImagePos:
    x: int
    y: int

    @staticmethod
    def from_dict(dict: dict):
        return ImagePos(**dict)

@dataclass
class PointPixelPos:
    image1: ImagePos | None = None
    image2: ImagePos | None = None

    @staticmethod
    def from_dict(dict: dict):
        return PointPixelPos(**{k: ImagePos.from_dict(v) for k, v in dict.items() if v is not None})

@dataclass
class ElementPixelPos:
    neutralPos: PointPixelPos = field(default_factory=PointPixelPos)
    pressedPos: PointPixelPos = field(default_factory=PointPixelPos)
    lowerPos: PointPixelPos = field(default_factory=PointPixelPos)

    @staticmethod
    def from_dict(dict: dict):
        return ElementPixelPos(**{k: PointPixelPos.from_dict(v) for k, v in dict.items()})

@dataclass
class PixelPositionOptions:
    pinky: ElementPixelPos = field(default_factory=ElementPixelPos)
    ringFinger: ElementPixelPos = field(default_factory=ElementPixelPos)
    middleFinger: ElementPixelPos = field(default_factory=ElementPixelPos)
    indexFinger: ElementPixelPos = field(default_factory=ElementPixelPos)
    thumb: ElementPixelPos = field(default_factory=ElementPixelPos)
    resetButton: ElementPixelPos = field(default_factory=ElementPixelPos)
    topSocket: ElementPixelPos = field(default_factory=ElementPixelPos)
    bottomSocket: ElementPixelPos = field(default_factory=ElementPixelPos)
    plate: ElementPixelPos = field(default_factory=ElementPixelPos)

    @staticmethod
    def from_dict(dict: dict):
        return PixelPositionOptions(**{k: ElementPixelPos.from_dict(v) for k, v in dict.items()})


def np_to_dict(arr: MatLike) -> dict:
    return {
        "dtype": arr.dtype,
        "bytes": base64.b64encode(arr),
        "shape": arr.shape
    }

def np_from_dict(dict: dict) -> MatLike:
    return np.frombuffer(
        base64.b64decode(dict["bytes"]),
        np.dtype(dict["dtype"])
    ).reshape(dict["shape"])


@dataclass
class CalibrationOptions:
    cameraMatrix1: MatLike
    distCoeffs1: MatLike
    cameraMatrix2: MatLike
    distCoeffs2: MatLike
    imageSize: MatLike
    R: MatLike
    T: MatLike
    E: MatLike
    F: MatLike

    @staticmethod
    def from_dict(dict: dict):
        return CalibrationOptions(**{k: np_from_dict(v) for k, v in dict.items()})
    
    def to_dict(self) -> dict:
        return {k: np_to_dict(v) for k, v in asdict(self).items()}

@dataclass
class AppOptions:
    positions: PixelPositionOptions = field(default_factory=PixelPositionOptions)
    calibration: CalibrationOptions = field(default_factory=CalibrationOptions)

    @staticmethod
    def from_dict(dict: dict):
        return AppOptions(
            positions= PixelPositionOptions.from_dict(dict["positions"]),
            calibration= CalibrationOptions.from_dict(dict["calibration"])
        )
    
    def to_dict(self) -> dict:
        return {
            "positions": asdict(self.positions),
            "calibration": self.calibration.to_dict()
        }

def main():
    a = AppOptions()
    a.positions.bottomSocket.lowerPos.image1 = ImagePos(1,1000000000)
    x = json.dumps(a.to_dict())
    print(x)
    print(AppOptions.from_dict(json.loads(x)))

if __name__ == "__main__":
    main()