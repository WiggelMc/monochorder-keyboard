from __future__ import annotations
from dataclasses import asdict, dataclass, field, fields
import os
import cv2
from cv2.typing import MatLike
import base64
import json
import numpy as np
import glob


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
        "dtype": arr.dtype.str,
        "bytes": base64.b64encode(arr).decode("ascii"),
        "shape": list(arr.shape)
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
        print(self)
        return {k: np_to_dict(v) for k, v in asdict(self).items()}

@dataclass
class ProjectOptions:
    calibration: CalibrationOptions
    positions: PixelPositionOptions = field(default_factory=PixelPositionOptions)

    @staticmethod
    def from_dict(dict: dict):
        return ProjectOptions(
            positions= PixelPositionOptions.from_dict(dict["positions"]),
            calibration= CalibrationOptions.from_dict(dict["calibration"])
        )
    
    def to_dict(self) -> dict:
        return {
            "positions": asdict(self.positions),
            "calibration": self.calibration.to_dict()
        }

@dataclass
class DoubleImage:
    image1: MatLike
    image2: MatLike


PROJECT_DIR = "projects"
OPTIONS_FILE = "properties.json"

def get_file_name(path: str):
    _, file_name = os.path.split(path)
    return file_name

def get_last_dir_name(path: str):
    dir_path, _ = os.path.split(path)
    _, dir_name = os.path.split(dir_path)
    return dir_name

@dataclass
class Project:
    name: str
    options: ProjectOptions
    images: list[DoubleImage]

    @staticmethod
    def list_all() -> list[str]:
        files = glob.glob(os.path.join(PROJECT_DIR,"*",OPTIONS_FILE))
        return [get_last_dir_name(file) for file in files]

    @staticmethod
    def load(name: str) -> Project:

        images: list[DoubleImage] = []
        image_files = glob.glob(os.path.join(PROJECT_DIR, name, "img_*_cam_*.png"))
        image_id_strings = {get_file_name(image_file).split("_")[1] for image_file in image_files}
        image_ids = [int(x) for x in image_id_strings if x.isdigit()]
        image_ids.sort()

        for image_id in image_ids:
            image1_path = os.path.join(PROJECT_DIR, name, f"img_{image_id}_cam_1.png")
            image2_path = os.path.join(PROJECT_DIR, name, f"img_{image_id}_cam_2.png")
            if (os.path.isfile(image1_path) and os.path.isfile(image2_path)):
                image1 = cv2.imread(image1_path)
                image2 = cv2.imread(image2_path)
                images.append(
                    DoubleImage(
                        image1=image1,
                        image2=image2
                    )
                )

        options: ProjectOptions
        with open(os.path.join(PROJECT_DIR, name, OPTIONS_FILE), "r") as file:
            options = ProjectOptions.from_dict(json.loads(file.read()))

        return Project(
            name=name,
            options=options,
            images=images
        )

    def exists(self) -> bool:
        return os.path.isfile(os.path.join(PROJECT_DIR, self.name, OPTIONS_FILE))

    def save_initial(self):
        if (not os.path.exists(os.path.join(PROJECT_DIR, self.name))):
            os.makedirs(os.path.join(PROJECT_DIR, self.name))
            
        self.save()

        for id, image in enumerate(self.images):
            cv2.imwrite(os.path.join(PROJECT_DIR, self.name, f"img_{id}_cam_1.png"), image.image1)
            cv2.imwrite(os.path.join(PROJECT_DIR, self.name, f"img_{id}_cam_2.png"), image.image2)

    def save(self):
        with open(os.path.join(PROJECT_DIR, self.name, OPTIONS_FILE), "w") as file:
            print(self.options.to_dict())
            file.write(json.dumps(self.options.to_dict(), indent=2))

# def main():
#     a = ProjectOptions()
#     a.positions.bottomSocket.lowerPos.image1 = ImagePos(1,1000000000)
#     x = json.dumps(a.to_dict())
#     print(x)
#     print(ProjectOptions.from_dict(json.loads(x)))

# if __name__ == "__main__":
#     main()