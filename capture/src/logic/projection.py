from typing import Sequence, cast
import cv2
from cv2.typing import MatLike, Rect, Size
import numpy as np
from itertools import chain

from logic.output import ElementPos, FingerPositionOptions, PositionOptions, SocketPositionOptions, Vector3
from logic.state import CalibrationOptions, PixelPositionOptions

def calibrate(patternSize: Size, squareWidth: float, image1: MatLike, image2: MatLike) -> CalibrationOptions:
    height1, width1 = image2.shape[:2]
    height2, width2 = image2.shape[:2]
    imageSize = np.array((min(width1, width2), min(height1, height2)), dtype=np.int32)

    scaledImage1 = cv2.resize(image1, imageSize)
    scaledImage2 = cv2.resize(image2, imageSize)

    objectPoints = np.array([[row * squareWidth, column * squareWidth, 0] for row in range(patternSize[0]) for column in range(patternSize[1])], dtype=np.float32)

    cameraMatrix1 = np.array([
        [imageSize[0], 0, imageSize[0] / 2],
        [0, imageSize[1], imageSize[1] / 2],
        [0, 0, 1]
    ], dtype=np.float64)
    distCoeffs1 = np.zeros(5, dtype=np.float64)
    cameraMatrix2 = cameraMatrix1.copy()
    distCoeffs2 = np.zeros(5, dtype=np.float64)

    retval1, corners1 = cast(
        typ=tuple[bool, MatLike],
        val=cv2.findChessboardCorners(scaledImage1, patternSize)
    )

    retval2, corners2 = cast(
        typ=tuple[bool, MatLike],
        val=cv2.findChessboardCorners(scaledImage2, patternSize)
    )

    print("got points", retval1, retval2)

    retval, cameraMatrix1, distCoeffs1, rvecs1, tvecs1 = cast(
        typ=tuple[float, MatLike, MatLike, Sequence[MatLike], Sequence[MatLike]],
        val=cv2.calibrateCamera([objectPoints], [corners1], imageSize, cameraMatrix1, distCoeffs1)
    )

    print("calibrated 1", retval)

    retval, cameraMatrix2, distCoeffs2, rvecs2, tvecs2 = cast(
        typ=tuple[float, MatLike, MatLike, Sequence[MatLike], Sequence[MatLike]],
        val=cv2.calibrateCamera([objectPoints], [corners2], imageSize, cameraMatrix2, distCoeffs2)
    )

    print("calibrated 1", retval)

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cast(
        typ=tuple[float, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike, MatLike],
        val=cv2.stereoCalibrate([objectPoints], [corners1], [corners2], cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize)
    )

    print("calibrated Both", retval)

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
        val=cv2.stereoRectify(c.cameraMatrix1, c.distCoeffs1, c.cameraMatrix2, c.distCoeffs2, c.imageSize, c.R, c.T)
    )

    outPointList = cast(
        typ=MatLike,
        val=cv2.triangulatePoints(R1, R2, imagePoints1, imagePoints2)
    )

    # TODO: Move Coordinate System Origin to thumb
    # subtract thumbNeutral from all

    # TODO: Rotate Positions so that axis line up (neutral -> press: z-) (neutral.xy -> lower.xy: x-)
    

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
