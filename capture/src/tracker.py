from enum import Enum
from typing import cast
import cv2
import numpy as np

from logic.camera import Camera
from logic.marker import MARKER_DICT, Marker
from cv2.typing import Size, MatLike, Point
from PIL import Image


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
    START = 0
    PRE_CALIBRATE = 1
    CALIBRATE = 2
    RECORD = 3

class CalibrationData:
    pass

def main():
    generate_charuco_image()
    generate_marker_image()

    cam = Camera.list()[1].connect()
    running = True
    stage = Stage.START
    calibration_data = None

    has_frame1, frame1 = False, None

    while running:
        has_frame, frame = cam.capture.read()

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False
        elif key == ord('c'):
            stage = Stage.CALIBRATE
        elif key == ord('s'):
            stage = Stage.START


        match stage:
            case Stage.START:
                has_frame1, frame1 = has_frame, detect(frame)
            case Stage.PRE_CALIBRATE:
                if has_frame:
                    has_frame1 = True
                    frame1 = detect(frame)
                    stage = Stage.CALIBRATE
            case Stage.CALIBRATE:
                ...
            case Stage.RECORD:
                has_frame1, frame1 = has_frame, frame

        if has_frame1:
            cv2.imshow("Window", frame1)



def detect(image: MatLike):
    params = cv2.aruco.DetectorParameters()
    refine_params = cv2.aruco.RefineParameters()
    detector = cv2.aruco.ArucoDetector(MARKER_DICT, params, refine_params)
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(image)
    if (len(markerCorners) >= 1):
        print(markerCorners[0].shape)
        print(markerCorners[0])

        object_points = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0]], dtype=np.float64)
        image_points = markerCorners[0][0]

        print(object_points)
        print(image_points)

        # retval, rvec, tvec = cast(
        #     typ=tuple[bool, MatLike, MatLike],
        #     val=cv2.solvePnP(object_points, image_points, "TODO", "TODO")
        # )

    image_copy = image.copy()
    cv2.aruco.drawDetectedMarkers(image_copy, markerCorners, markerIds)
    return image_copy

def calibrate(image: MatLike):
    ...

def generate_charuco_image():
    size: Size = (7, 5)
    margin = round(15 * a4_dpmm)

    charuco_board = cv2.aruco.CharucoBoard(size=size, squareLength=1, markerLength=0.8, dictionary=MARKER_DICT)
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
    main()