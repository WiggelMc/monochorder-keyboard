from typing import NamedTuple, Sequence
import numpy as np


class CharucoBoard_MatchImagePoints(NamedTuple):
    object_points: np.ndarray
    image_points: np.ndarray

class CharucoDetector_DetectBoard(NamedTuple):
    charucoCorners: np.ndarray
    charucoIds: np.ndarray
    markerCorners: Sequence[np.ndarray]
    markerIds: np.ndarray

class ArucoDetector_DetectMarkers(NamedTuple):
    markerCorners: Sequence[np.ndarray]
    markerIds: np.ndarray
    rejectedCandidates: Sequence[np.ndarray]

class CV_SolvePnP(NamedTuple):
    retval: bool
    rvec: np.ndarray
    tvec: np.ndarray

class CV_CalibrateCamera(NamedTuple):
    retval: float
    cameraMatrix: np.ndarray
    distCoeffs: np.ndarray
    rvecs: Sequence[np.ndarray]
    tvecs: Sequence[np.ndarray]