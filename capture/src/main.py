from dataclasses import dataclass
from typing import Any
import cv2
from pygrabber.dshow_graph import FilterGraph

@dataclass
class Camera:
    id: int
    name: str
    capture: cv2.VideoCapture


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
                cv2.imshow(f"{cam.name} ({cam.id})", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False


if __name__ == "__main__":
    main()