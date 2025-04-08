from dataclasses import dataclass
from typing import Any, Sequence, cast
import cv2
from cv2.typing import MatLike, Rect
import numpy as np
from pygrabber.dshow_graph import FilterGraph
import tkinter as tk
from itertools import chain

from logic.output import ElementPos, FingerPositionOptions, PositionOptions, SocketPositionOptions, Vector3
from logic.state import CalibrationOptions, PixelPositionOptions

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



# Rows: int
# Columns: int
# squareWidth: float
# [calibrate]

# [snap] -> [Keep|Discard]

# Name: str
# [Save and Quit]



# Name: list
# [Open]

# Image: list
# Object: "pinky" | ...
# Variant: "neutral" | "pressed" | "lower"
# [Save]
# []


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