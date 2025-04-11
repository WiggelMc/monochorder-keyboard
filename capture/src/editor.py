from dataclasses import dataclass
from enum import Enum
from queue import Queue
from threading import Thread
import tkinter as tk
from tkinter import ttk
from typing import Callable

import cv2
from cv2.typing import MatLike, Rect
import numpy as np

from logic.camera import Camera, ConnectedCamera
from logic.projection import calibrate, projectPoints
from logic.state import DoubleImage, ElementPixelPos, ImagePos, PixelPositionOptions, PointPixelPos, Project, ProjectOptions

class PosObject(Enum):
    PINKY = 0
    RING_FINGER = 1
    MIDDLE_FINGER = 2
    INDEX_FINGER = 3
    THUMB = 4
    RESET_BUTTON = 5
    TOP_SOCKET = 6
    BOTTOM_SOCKET = 7
    PLATE = 8

    def succ(self):
        return PosObject((self.value + 1) % len(PosObject))
    
    def pred(self):
        return PosObject((self.value - 1) % len(PosObject))

class PosVariant(Enum):
    NEUTRAL = 0
    PRESSED = 1
    LOWER = 2

    def succ(self):
        return PosVariant((self.value + 1) % len(PosVariant))
    
    def pred(self):
        return PosVariant((self.value - 1) % len(PosVariant))

class PosImage(Enum):
    IMAGE_1 = 0
    IMAGE_2 = 1

@dataclass
class State:
    project: Project | None = None
    running: bool = True
    selected_image: int = 0
    selected_object: PosObject = PosObject.PINKY
    selected_variant: PosVariant = PosVariant.NEUTRAL
    hover_image: PosImage = PosImage.IMAGE_1
    render_window: Callable | None = None

state: State = State()

def tk_main():
    root = tk.Tk()
    root.title("Monochorder Capture Edit")
    root.geometry("400x300")

    def clear():
        for widget in root.winfo_children():
            widget.destroy()

    def render_load_project():
        clear()

        projects = Project.list_all()

        row = 0
        project_var = tk.StringVar()
        tk.Label(root, text="Project").grid(row=row, column=0)
        ttk.Combobox(root, values=projects, textvariable=project_var).grid(row=row, column=1)

        def submit():
            state.project = Project.load(project_var.get())
            state.render_window = render_editing
            render_editing()

        row += 1
        tk.Button(root, text="Open", command=submit).grid(row=row, column=0, columnspan=2, pady=20)

    def render_editing():
        clear()

        row = 0
        tk.Label(root, text="Image").grid(row=row, column=0)
        tk.Label(root, text=str(state.selected_image)).grid(row=row, column=1)

        row += 1
        tk.Label(root, text="Object").grid(row=row, column=0)
        tk.Label(root, text=str(state.selected_object)).grid(row=row, column=1)

        row += 1
        tk.Label(root, text="Variant").grid(row=row, column=0)
        tk.Label(root, text=str(state.selected_variant)).grid(row=row, column=1)

        def save():
            try:
                state.project.save()
            except Exception as e:
                print(e)

        def export():
            try:
                positions = projectPoints(state.project.options.calibration, state.project.options.positions)
                positions.export(state.project.name)
            except Exception as e:
                print(e)

        row += 1
        tk.Button(root, text="Save", command=save).grid(row=row, column=0, columnspan=2, pady=20)
        row += 1
        tk.Button(root, text="Export", command=export).grid(row=row, column=0, columnspan=2, pady=20)

    render_load_project()
    root.mainloop()
    
    state.running = False

def get_object(options: PixelPositionOptions, selected: PosObject) -> ElementPixelPos:
    if selected == PosObject.PINKY:
        return options.pinky
    elif selected == PosObject.RING_FINGER:
        return options.ringFinger
    elif selected == PosObject.MIDDLE_FINGER:
        return options.middleFinger
    elif selected == PosObject.INDEX_FINGER:
        return options.indexFinger
    elif selected == PosObject.THUMB:
        return options.thumb
    elif selected == PosObject.RESET_BUTTON:
        return options.resetButton
    elif selected == PosObject.TOP_SOCKET:
        return options.topSocket
    elif selected == PosObject.BOTTOM_SOCKET:
        return options.bottomSocket
    elif selected == PosObject.PLATE:
        return options.plate
    
def get_variant(pos: ElementPixelPos, selected: PosVariant) -> PointPixelPos:
    if selected == PosVariant.NEUTRAL:
        return pos.neutralPos
    elif selected == PosVariant.PRESSED:
        return pos.pressedPos
    elif selected == PosVariant.LOWER:
        return pos.lowerPos

def set_point(pos: ImagePos | None, image: PosImage):
    object = get_object(state.project.options.positions, state.selected_object)
    pixelPos = get_variant(object, state.selected_variant)

    if image == PosImage.IMAGE_1:
        pixelPos.image1 = pos
    elif image == PosImage.IMAGE_2:
        pixelPos.image2 = pos

def on_mouse(event: int, x: int, y: int, flags: int, image: PosImage):
    state.hover_image = image
    if event == cv2.EVENT_LBUTTONDOWN: 
        set_point(ImagePos(x, y), image)

def cv_main():
    while state.running:
        if state.project is not None:
            if state.selected_image <= len(state.project.images):
                image = state.project.images[state.selected_image]
                cv2.imshow("Image 1", image.image1)
                cv2.imshow("Image 2", image.image2)
                cv2.setMouseCallback("Image 1", on_mouse, PosImage.IMAGE_1)
                cv2.setMouseCallback("Image 2", on_mouse, PosImage.IMAGE_2)
            
            key = cv2.waitKey(1) & 0xFF

            refresh = True

            if key == ord('s'):
                state.selected_image = (state.selected_image - 1) % len(state.project.images)
            elif key == ord('w'):
                state.selected_image = (state.selected_image + 1) % len(state.project.images)
            elif key == ord('a'):
                state.selected_object = state.selected_object.pred()
            elif key == ord('d'):
                state.selected_object = state.selected_object.succ()
            elif key == ord('q'):
                state.selected_variant = state.selected_variant.pred()
            elif key == ord('e'):
                state.selected_variant = state.selected_variant.succ()
            elif key == 0x08:
                set_point(None, state.hover_image)
            else:
                refresh = False

            if refresh and state.render_window is not None:
                state.render_window()


def main():
    t1 = Thread(target=tk_main)
    t2 = Thread(target=cv_main)

    t1.start()
    t2.start()

if __name__ == "__main__":
    main()