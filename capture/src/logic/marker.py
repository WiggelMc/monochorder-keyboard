from enum import Enum

import cv2


MARKER_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
MARKER_WIDTH_MM = 10

class Marker(Enum):
    PINKY = 10
    RING_FINGER = 11
    MIDDLE_FINGER = 12
    INDEX_FINGER = 13
    THUMB = 14
    RESET_BUTTON = 15
    TOP_SOCKET = 16
    BOTTOM_SOCKET = 17
    PLATE = 18