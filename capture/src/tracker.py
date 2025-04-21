from dataclasses import dataclass
from enum import Enum
import os
from typing import cast
import cv2
import numpy as np

from logic.camera import Camera, ConnectedCamera
from logic.marker import MARKER_DICT, Marker
from cv2.typing import Size, MatLike, Point
from PIL import Image

from logic.opencv import ArucoDetector_DetectMarkers, CV_CalibrateCamera, CV_SolvePnP, CharucoBoard_MatchImagePoints, CharucoDetector_DetectBoard


a4_size: Size = (3508, 2480)
a4_dpi = 300
a4_dpmm = a4_dpi * 0.0394

def save_image(filename: str, image: MatLike, dpi: int):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_pil.save(filename, dpi=(dpi, dpi))


def marker_patch_size(size: int) -> Size:
    return (round(size * 1.2), round(size * 1.2 + 30))


def place_marker(image: MatLike, marker: Marker, size: int, point: Point):
    marker_gray = cv2.aruco.generateImageMarker(MARKER_DICT, marker.marker_id, sidePixels=size)
    marker_image = cv2.cvtColor(marker_gray, cv2.COLOR_GRAY2BGR)
    
    pw, ph = marker_patch_size(size)

    h, w = marker_image.shape[:2]
    x, y = point

    wo, ho = (pw - w) // 2, (ph - h) // 2

    image[ho+y:ho+y+h, wo+x:wo+x+w] = marker_image

    cv2.rectangle(image, point, (x+pw, y+ph), (20, 20, 20), 2)
    cv2.putText(image, marker.display_name, (wo+x, ho+y+h+20), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


class Stage(Enum):
    CALIBRATE = (0, "Calibration", ["Space: Snap", "d: Start Detection"])
    CALIBRATE_SNAP = (1, "Calibration Image", ["Enter: Accept", "Backspace: Reject"])
    DETECT = (2, "Detection", ["Space: Snap"])
    DETECT_SNAP = (3, "Detection Image", ["Enter: Save", "Backspace: Discard"])

    mode_id: int
    mode_name: str
    controls: list[str]

    def __init__(self, mode_id: int, mode_name: str, controls: str):
        self.mode_id = mode_id
        self.mode_name = mode_name
        self.controls = controls

    @property
    def description(self):
        return f"{self.mode_name}: [{''.join(c + ', ' for c in self.controls)}r: Reset, q: Quit]"

class CalibrationData:
    pass

KEYCODE_SPACE = 0x20
KEYCODE_ENTER = 0x0D
KEYCODE_BACKSPACE = 0x08

class Keymap:
    accept = KEYCODE_ENTER
    reject = KEYCODE_BACKSPACE
    snap = KEYCODE_SPACE
    detect = ord('d')
    quit = ord('q')
    reset = ord('r')


WINDOW_NAME = "App Window"

@dataclass
class Config:
    cam: Camera
    name: str


def get_test_config() -> Config:
    return Config(
        cam=Camera.list()[1],
        name="Test"
    )


def get_config() -> Config:
    cameras = Camera.list()
    print("\nConnected Cameras:\n")
    print("\n".join([f"{c.id: >4}: {c.name}" for c in cameras]))
    print("\n")

    cam: Camera | None = None

    while cam is None:
        try:
            cam_input = input("Cam: ")
            cam = next((c for c in cameras if c.id == int(cam_input)), None)
            if cam is None:
                raise IndexError("Invalid Camera Index")
        except Exception as e:
            print(e)

    name = input("Name: ")

    return Config(
        cam=cam,
        name=name
    )

def run_app():
    running: bool = True
    while running:
        running = app()
        cv2.destroyWindow(WINDOW_NAME)

def app() -> bool:
    config = get_test_config()
    cam: ConnectedCamera = config.cam.connect()
    running: bool = True
    calibration_data: CalibrationData | None = None
    stage: Stage = Stage.CALIBRATE

    def set_stage(new_stage: Stage):
        nonlocal stage
        stage = new_stage
        print()
        print(new_stage.description)

    set_stage(Stage.CALIBRATE)

    has_cam_frame: bool = False
    cam_frame: MatLike = []

    while not has_cam_frame:
        has_cam_frame, cam_frame = cam.capture.read()
        cv2.waitKey(1)
    
    window_frame: MatLike = cam_frame

    while running:
        has_new_frame, new_frame = cam.capture.read()
        if has_new_frame:
            cam_frame = new_frame

        key = cv2.waitKey(1) & 0xFF

        if key == Keymap.quit:
            return False
        elif key == Keymap.reset:
            return True
        
        match stage:
            case Stage.CALIBRATE:
                window_frame = detect(cam_frame)
                # detect image points

                if key == Keymap.snap:
                    # report image point feedback
                    set_stage(Stage.CALIBRATE_SNAP)

                elif key == Keymap.detect:
                    # report calibration accuracy
                    # report that calibration is finished
                    set_stage(Stage.DETECT)

            case Stage.CALIBRATE_SNAP:
                if key == Keymap.accept:
                    # run calibration on image (if possible)
                    # report calibration accuracy
                    set_stage(Stage.CALIBRATE)

                elif key == Keymap.reject:
                    # report rejection
                    set_stage(Stage.CALIBRATE)

            case Stage.DETECT:
                window_frame = detect(cam_frame)
                # detect image points

                if key == Keymap.snap:
                    # run 3d detection
                    # report detection results
                    set_stage(Stage.DETECT_SNAP)

            case Stage.DETECT_SNAP:
                if key == Keymap.accept:
                    # save file
                    # report filename and location
                    set_stage(Stage.DETECT)


                elif key == Keymap.reject:
                    # report rejection
                    set_stage(Stage.DETECT)

        cv2.imshow(WINDOW_NAME, window_frame)

        




        




OUT_DIR = "out"

def main():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    generate_charuco_image()
    generate_marker_image()

    cam = Camera.list()[1].connect()
    running = True
    stage = Stage.CALIBRATE
    calibration_data = None

    has_loaded_frame, loaded_frame = False, None

    while running:
        has_frame, frame = cam.capture.read()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False
        elif key == ord('c'):
            stage = Stage.CALIBRATE_SNAP
        elif key == ord('r'):
            stage = Stage.CALIBRATE
        elif key == ord('d'):
            stage = Stage.DETECT
        elif key == KEYCODE_SPACE:
            match stage:
                case Stage.CALIBRATE:
                    stage = Stage.CALIBRATE_SNAP
                case Stage.DETECT:
                    stage = Stage.DETECT_SNAP
        elif key == KEYCODE_ENTER:
            match stage:
                case Stage.CALIBRATE_IDLE:
                    stage = Stage.CALIBRATE_SNAP
                case Stage.DETECT_IDLE:
                    stage = Stage.DETECT_SNAP



        print(key)


        match stage:
            case Stage.CALIBRATE:
                if has_frame:
                    has_loaded_frame, loaded_frame = has_frame, detect(frame)
            case Stage.CALIBRATE_SNAP:
                if has_frame:
                    has_loaded_frame = True
                    loaded_frame = detect(frame)
                    stage = Stage.CALIBRATE
            case Stage.DETECT:
                ...
            case Stage.DETECT_SNAP:
                has_loaded_frame, loaded_frame = has_frame, frame

        if has_loaded_frame:
            cv2.imshow("Window", loaded_frame)



def detect(image: MatLike):
    params = cv2.aruco.DetectorParameters()
    refine_params = cv2.aruco.RefineParameters()
    detector = cv2.aruco.ArucoDetector(MARKER_DICT, params, refine_params)
    r = ArucoDetector_DetectMarkers(*detector.detectMarkers(image))
    if (len(r.markerCorners) >= 1):
        print(r.markerCorners[0].shape)
        print(r.markerCorners[0])

        object_points = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0]], dtype=np.float64)
        image_points = r.markerCorners[0][0]

        print(object_points)
        print(image_points)

        # c = CV_SolvePnP(*cv2.solvePnP(object_points, image_points, "TODO", "TODO"))

    image_copy = image.copy()
    cv2.aruco.drawDetectedMarkers(image_copy, r.markerCorners, r.markerIds)
    return image_copy

def calibrate(image: MatLike):
    charuco_board = get_charuco_board()

    object_points = charuco_board.getObjPoints()

    charuco_params = cv2.aruco.CharucoParameters()
    params = cv2.aruco.DetectorParameters()
    refine_params = cv2.aruco.RefineParameters()

    detector = cv2.aruco.CharucoDetector(MARKER_DICT, charuco_params, params, refine_params)
    detectionResult = CharucoDetector_DetectBoard(*detector.detectBoard(image))


    charuco_board.det
    m = CharucoBoard_MatchImagePoints(*charuco_board.matchImagePoints(
        detectionResult.charucoCorners,
        detectionResult.charucoIds
    ))

    x = CV_CalibrateCamera(*cv2.calibrateCamera(
        *"TODO"
    ))


def get_charuco_board():
    size: Size = (7, 5)

    return cv2.aruco.CharucoBoard(size=size, squareLength=1, markerLength=0.8, dictionary=MARKER_DICT)

def generate_charuco_image():
    charuco_board = get_charuco_board()
    margin = round(15 * a4_dpmm)

    charuco_image = charuco_board.generateImage(outSize=a4_size, marginSize=margin)

    save_image("out/charuco.png", charuco_image, a4_dpi)


def generate_marker_image():
    margin = round(15 * a4_dpmm)
    duplicates = 7

    marker_image = np.full((a4_size[1], a4_size[0], 3), 255, dtype=np.uint8)
    marker_size = round(10 * a4_dpmm)
    
    pw, ph = marker_patch_size(marker_size)
    wo, ho = pw + round(3 * a4_dpmm), ph + round(3 * a4_dpmm)

    for i, marker in enumerate(Marker):
        for j in range(duplicates):
            place_marker(marker_image, marker, marker_size, (margin+i*wo, margin+j*ho))

    save_image("out/markers.png", marker_image, a4_dpi)


if __name__ == "__main__":
    run_app()