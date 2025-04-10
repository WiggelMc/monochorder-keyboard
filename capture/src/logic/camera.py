from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Sequence, cast
import cv2
from cv2.typing import MatLike, Rect
import numpy as np
from pygrabber.dshow_graph import FilterGraph
import tkinter as tk
from itertools import chain

@dataclass
class Camera:
    id: int
    name: str

    def connect(self) -> ConnectedCamera:
        return ConnectedCamera(
            camera=self,
            capture=cv2.VideoCapture(self.id)
        )
    
    @staticmethod
    def list() -> list[Camera]:
        return [Camera(id, name) for id, name in enumerate(FilterGraph().get_input_devices())]

@dataclass
class ConnectedCamera:
    camera: Camera
    capture: cv2.VideoCapture

    def render(self, window: str):
        has_frame, frame = self.capture.read()

        if has_frame:
            cv2.imshow(window, frame)

        cv2.waitKey(1)






