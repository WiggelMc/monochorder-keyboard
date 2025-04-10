from dataclasses import dataclass
from queue import Queue
from threading import Thread
import tkinter as tk
from tkinter import ttk

import cv2

from logic.camera import Camera, ConnectedCamera

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

            render_image_creation(cam1A, cam2A)

        row += 1
        tk.Button(root, text="Calibrate [C]", command=submit).grid(row=row, column=0, columnspan=2, pady=20)

    def render_image_creation(cam1: ConnectedCamera, cam2: ConnectedCamera):
        global cv_state
        clear()

        name_var = tk.StringVar()
        tk.Label(root, text="Name").grid(row=0, column=0)
        tk.Entry(root, validate="key", validatecommand=vcmd_filename, textvariable=name_var).grid(row=0, column=1, pady=5)

        cv_state = CVState(
            cam1=cam1,
            cam2=cam2,
            shot=False
        )

        def submit():
            print(name_var.get())
            root.quit()

        tk.Button(root, text="Save and Quit [C]", command=submit).grid(row=1, column=0, columnspan=2, pady=20)

    render_calibration()
    root.mainloop()
    
    global running
    running = False


@dataclass
class CVState:
    cam1: ConnectedCamera
    cam2: ConnectedCamera
    shot: bool

cv_state: CVState | None = None
running = True

def cv_main():
    while running:
        if cv_state is not None:
            has_frame1, frame1 = cv_state.cam1.capture.read()
            if has_frame1:
                cv2.imshow("Cam 1", frame1)

            has_frame2, frame2 = cv_state.cam2.capture.read()
            if has_frame2:
                cv2.imshow("Cam 2", frame2)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv_state.shot = True

            if (cv_state.shot and has_frame1 and has_frame2):
                cv2.imshow("Image 1", frame1)
                cv2.imshow("Image 2", frame2)
                cv_state.shot = False


def main():
    t1 = Thread(target=tk_main)
    t2 = Thread(target=cv_main)

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()