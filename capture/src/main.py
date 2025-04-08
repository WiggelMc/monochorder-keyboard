from dataclasses import dataclass
from typing import Any, Sequence, cast
import cv2
from cv2.typing import MatLike, Rect
import numpy as np
from pygrabber.dshow_graph import FilterGraph
import tkinter as tk
from itertools import chain

from output import ElementPos, FingerPositionOptions, PositionOptions, SocketPositionOptions, Vector3
from state import CalibrationOptions, PixelPositionOptions

@dataclass
class Camera:
    id: int
    name: str
    capture: cv2.VideoCapture

def select_point(event: int, x: int, y: int, flags: int, name: str):    
    print(f"{name}: ({event}, {x}, {y}, {flags:>08b})")

def main():

    root = tk.Tk()
    button = tk.Button(root, text="Hello")
    button2 = tk.Button(root, text="Hello")
    button.grid(row=0, column=0)
    button2.grid(row=0, column=1)

    root.mainloop()
    return

    devices = FilterGraph().get_input_devices()
    print("\nConnected Cameras:\n")
    print("\n".join([f"{i: >4}: {name}" for i, name in enumerate(devices)]))
    print("\n")

    cam1_id = input("Cam 1: ")
    cam2_id = input("Cam 2: ")

    cam_ids = [int(cam1_id), int(cam2_id)]
    cams = [Camera(id, devices[id], cv2.VideoCapture(id)) for id in cam_ids]


    print("\nSelected Cameras:\n")
    print("\n".join([f"{cam.id: >4}: {cam.name}" for cam in cams]))
    print("\n")

    running = True

    while running:
        for cam in cams:
            has_frame, frame = cam.capture.read()

            if has_frame:
                window_name = f"{cam.name} ({cam.id})"
                cv2.imshow(window_name, frame)
                cv2.setMouseCallback(window_name, select_point, window_name)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False


if __name__ == "__main__":
    main()


def calibrate(patternSize: MatLike, squareWidth: float, image1: MatLike, image2: MatLike) -> CalibrationOptions:
    height1, width1 = image2.shape[:2]
    height2, width2 = image2.shape[:2]
    imageSize = np.array((min(width1, width2), min(height1, height2)), dtype=np.float64)

    scaledImage1 = cv2.resize(image1, imageSize)
    scaledImage2 = cv2.resize(image2, imageSize)

    objectPoints = [[row * squareWidth, column * squareWidth] for row in range(patternSize[0]) for column in range(patternSize[1])]

    cameraMatrix1 = np.array([
        [imageSize[0], 0, imageSize[0] / 2],
        [0, imageSize[1], imageSize[1] / 2],
        [0, 0, 1]
    ], dtype=np.float64)
    distCoeffs1 = np.zeros(5, dtype=np.float64)
    cameraMatrix2 = cameraMatrix1.copy()
    distCoeffs2 = np.zeros(5, dtype=np.float64)

    retval, corners1 = cast(
        typ=tuple[bool, MatLike],
        val=cv2.findChessboardCorners(scaledImage1, patternSize)
    )

    retval, corners2 = cast(
        typ=tuple[bool, MatLike],
        val=cv2.findChessboardCorners(scaledImage2, patternSize)
    )

    retval, cameraMatrix1, distCoeffs1, rvecs1, tvecs1 = cast(
        typ=tuple[float, MatLike, MatLike, Sequence[MatLike], Sequence[MatLike]],
        val=cv2.calibrateCamera(objectPoints, corners1, imageSize, cameraMatrix1, distCoeffs1)
    )

    retval, cameraMatrix2, distCoeffs2, rvecs2, tvecs2 = cast(
        typ=tuple[float, MatLike, MatLike, Sequence[MatLike], Sequence[MatLike]],
        val=cv2.calibrateCamera(objectPoints, corners2, imageSize, cameraMatrix2, distCoeffs2)
    )

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cast(
        typ=tuple[float, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike],
        val=cv2.stereoCalibrate(objectPoints, corners1, corners2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize)
    )

    return CalibrationOptions(
        cameraMatrix1=cameraMatrix1,
        distCoeffs1=distCoeffs1,
        cameraMatrix2=cameraMatrix2,
        distCoeffs2=distCoeffs2,
        imageSize=imageSize,
        R=R,
        T=T,
        E=E,
        F=F
    )

def projectPoints(calibration: CalibrationOptions, positions: PixelPositionOptions) -> PositionOptions:
    c = calibration

    positionList = list(chain.from_iterable((
        (
            pos.neutralPos,
            pos.pressedPos,
            pos.lowerPos
        ) for pos in (
            positions.pinky,
            positions.ringFinger,
            positions.middleFinger,
            positions.indexFinger,
            positions.thumb,
            positions.resetButton,
            positions.topSocket,
            positions.bottomSocket,
            positions.plate
        )
    )))

    imagePoints1 = np.array(
        [[pos.image1.x, pos.image1.y] for pos in positionList],
        dtype=np.float64
    )
    imagePoints2 = np.array(
        [[pos.image2.x, pos.image2.y] for pos in positionList],
        dtype=np.float64
    )

    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cast(
        typ=tuple[MatLike, MatLike, MatLike, MatLike, MatLike, Rect, Rect],
        val=cv2.stereoRectify(c.cameraMatrix1, c.distCoeffs1, c.cameraMatrix2, c.distCoeffs2, c.imageSize, c.R)
    )

    outPointList = cast(
        typ=MatLike,
        val=cv2.triangulatePoints(R1, R2, imagePoints1, imagePoints2)
    )

    outVectorList = [Vector3(x,y,z) for point in outPointList for [x, y, z] in point]

    outPositionList = [
        ElementPos(neutralPos, pressedPos, lowerPos)
        for [neutralPos, pressedPos, lowerPos] in
        (
            outVectorList[i:i+3] 
            for i in range(0, len(outPointList), 3)
        )
    ]

    return PositionOptions(
        finger= FingerPositionOptions(
            pinky=outPositionList[0],
            ringFinger=outPositionList[1],
            middleFinger=outPositionList[2],
            indexFinger=outPositionList[3],
            thumb=outPositionList[4],
            resetButton=outPositionList[5]
        ),
        socket= SocketPositionOptions(
            topSocket=outPositionList[6],
            bottomSocket=outPositionList[7],
        ),
        plate=outPositionList[8]
    )

# Steps:
# - Select Cams
# - Select Hand
# - Make Calibration Photos (Calibrate)
# - Make Photos (as many as needed) (All Photos are in the same coordinate system)
# - Save Photos to Disk
# - Select Points (Scroll through Photos) (Points are shared between Photos and Labeled)
# - Save Points (json, txt) (always saves both, json for editing, txt for copying into ts)

# Json Cordinate System:
# - save points in px
# - save calibration data in json

# TypeScript Coordinate System:
# - Thumb Neutral is Origin
# - Thumb Press is in Y Direction
# - Thumb Lower is in Z Direction


# TODO:
# - formatter
# - ui
# - math


# 	cv.triangulatePoints(	projMatr1, projMatr2, projPoints1, projPoints2[, points4D]	) 
# -> 	points4D

# 	cv.stereoRectify(	cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T[, R1[, R2[, P1[, P2[, Q[, flags[, alpha[, newImageSize]]]]]]]]	) 
# -> 	R1, R2, P1, P2, Q, validPixROI1, validPixROI2

# cv.stereoCalibrate(	objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize[, R[, T[, E[, F[, flags[, criteria]]]]]]	) 
# -> 	retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F

# cv.stereoCalibrateExtended(	objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T[, E[, F[, perViewErrors[, flags[, criteria]]]]]	) 
# -> 	retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F, perViewErrors