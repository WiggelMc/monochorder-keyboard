from dataclasses import dataclass
from queue import Queue
from threading import Thread
import tkinter as tk
from tkinter import ttk

import cv2
from cv2.typing import MatLike, Rect
import numpy as np

from logic.camera import Camera, ConnectedCamera
from logic.projection import calibrate
from logic.state import DoubleImage, Project, ProjectOptions

@dataclass
class CalibrateState:
    cam1: ConnectedCamera
    cam2: ConnectedCamera
    name: str
    patternSize: MatLike
    squareWidth: float

@dataclass
class State:
    calibrate: CalibrateState | None
    project: Project | None
    running: bool
    makeImage: bool


state: State = State(
    calibrate=None,
    project=None,
    running=True,
    makeImage=False
)

def only_int(input: str):
    return input.isdigit()

def only_filename(input: str):
    return input.isalpha() or input.isnumeric() or input in ["-", "_"]

def only_float(input: str):
    return input.isdigit() or input == "."

def tk_main():
    root = tk.Tk()
    root.title("Monochorder Capture Setup")
    root.geometry("400x300")

    vcmd_int = (root.register(only_int), '%S')
    vcmd_float = (root.register(only_float), '%S')
    vcmd_filename = (root.register(only_filename), '%S')

    def clear():
        for widget in root.winfo_children():
            widget.destroy()

    def render_calibration():
        clear()

        cams = Camera.list()
        cam_names = [f"{cam.id} - {cam.name}" for cam in cams]

        row = 0
        cam1_var = tk.StringVar()
        tk.Label(root, text="Cam 1").grid(row=row, column=0)
        ttk.Combobox(root, state="readonly", values=cam_names, textvariable=cam1_var).grid(row=row, column=1)

        row += 1
        cam2_var = tk.StringVar()
        tk.Label(root, text="Cam 2").grid(row=row, column=0)
        ttk.Combobox(root, state="readonly", values=cam_names, textvariable=cam2_var).grid(row=row, column=1)

        row += 1
        rows_var = tk.StringVar()
        tk.Label(root, text="Rows").grid(row=row, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=rows_var).grid(row=row, column=1, pady=5)

        row += 1
        columns_var = tk.StringVar()
        tk.Label(root, text="Columns").grid(row=row, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_int, textvariable=columns_var).grid(row=row, column=1, pady=5)

        row += 1
        square_width_var = tk.StringVar()
        tk.Label(root, text="Square Width").grid(row=row, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_float, textvariable=square_width_var).grid(row=row, column=1, pady=5)

        row += 1
        name_var = tk.StringVar()
        tk.Label(root, text="Name").grid(row=row, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_filename, textvariable=name_var).grid(row=row, column=1, pady=5)

        def submit():
            print(int(rows_var.get()))
            print(int(columns_var.get()))
            print(float(square_width_var.get()))

            cam1_id = int(cam1_var.get().split("-")[0])
            cam1 = next((cam for cam in cams if cam.id == cam1_id), None)
            print(cam1)

            cam2_id = int(cam2_var.get().split("-")[0])
            cam2 = next((cam for cam in cams if cam.id == cam2_id), None)
            print(cam2)

            cam1A = cam1.connect()
            cam2A = cam2.connect()

            state.calibrate = CalibrateState(
                cam1=cam1A,
                cam2=cam2A,
                name=name_var.get(),
                patternSize=np.array([int(rows_var.get()), int(columns_var.get())]),
                squareWidth=float(square_width_var.get())
            )

            render_image_creation(cam1A, cam2A)

        row += 1
        tk.Button(root, text="Calibrate [C]", command=submit).grid(row=row, column=0, columnspan=2, pady=20)

    def render_image_creation(cam1: ConnectedCamera, cam2: ConnectedCamera):
        clear()

        def submit():
            root.quit()

        tk.Button(root, text="Save and Quit [C]", command=submit).grid(row=1, column=0, columnspan=2, pady=20)

    render_calibration()
    root.mainloop()
    
    state.running = False

def cv_main():
    while state.running:
        if state.calibrate is not None:
            has_frame1, frame1 = state.calibrate.cam1.capture.read()
            if has_frame1:
                cv2.imshow("Cam 1", frame1)

            has_frame2, frame2 = state.calibrate.cam2.capture.read()
            if has_frame2:
                cv2.imshow("Cam 2", frame2)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                state.makeImage = True

            if (state.makeImage and has_frame1 and has_frame2):
                cv2.imshow("Image 1", frame1)
                cv2.imshow("Image 2", frame2)

                if state.project is None:

                    calibration = calibrate(
                        patternSize=state.calibrate.patternSize,
                        squareWidth=state.calibrate.squareWidth,
                        image1=frame1,
                        image2=frame2
                    )
                    state.project = Project(
                        name=state.calibrate.name,
                        options=ProjectOptions(calibration=calibration),
                        images=[]
                    )
                else:
                    pass
                    

                state.makeImage = False


def main():
    t1 = Thread(target=tk_main)
    t2 = Thread(target=cv_main)

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()