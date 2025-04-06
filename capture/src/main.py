from dataclasses import dataclass
from typing import Any
import cv2
from pygrabber.dshow_graph import FilterGraph

@dataclass
class Camera:
    id: int
    name: str
    capture: cv2.VideoCapture

def select_point(event: int, x: int, y: int, flags: int, name: str):    
    print(f"{name}: ({event}, {x}, {y}, {flags:>08b})")

def main():

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
