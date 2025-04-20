from __future__ import annotations
from enum import Enum

import cv2


MARKER_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
MARKER_WIDTH_MM = 10

class Marker(Enum):
    PINKY = ("Pinky", 10)
    RING_FINGER = ("Ring Finger", 11)
    MIDDLE_FINGER = ("Middle Finger", 12)
    INDEX_FINGER = ("Index Finger", 13)
    THUMB = ("Thumb", 14)
    RESET_BUTTON = ("Reset Button", 15)
    TOP_SOCKET = ("Top Socket", 16)
    BOTTOM_SOCKET = ("Bottom Socket", 17)
    PLATE = ("Plate", 18)

    display_name: str
    marker_id: int

    def __init__(self, display_name: str, marker_id: int):
        self.display_name = display_name
        self.marker_id = marker_id

    @classmethod
    def from_marker_id(cls, marker_id: int) -> Marker | None:
        return next((m for m in cls if m.marker_id == marker_id), None)