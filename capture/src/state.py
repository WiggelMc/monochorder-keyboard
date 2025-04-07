from dataclasses import asdict, dataclass, field, fields
import json


@dataclass
class ImagePos:
    x: int
    y: int

    @staticmethod
    def from_dict(dict: dict):
        return ImagePos(**dict)

@dataclass
class PointPixelPos:
    imageA: ImagePos | None = None
    imageB: ImagePos | None = None

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

@dataclass
class CalibrationOptions:
    pass

    @staticmethod
    def from_dict(dict: dict):
        return CalibrationOptions(**dict)

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

def main():
    a = AppOptions()
    a.positions.bottomSocket.lowerPos.imageA = ImagePos(1,1000000000)
    x = json.dumps(asdict(a))
    print(x)
    print(AppOptions.from_dict(json.loads(x)))

if __name__ == "__main__":
    main()