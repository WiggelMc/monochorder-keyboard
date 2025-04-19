import cv2
import numpy as np

from logic.marker import MARKER_DICT, Marker
from cv2.typing import Size, MatLike, Point
from PIL import Image


a4_size: Size = (3508, 2480)
a4_dpi = 300
a4_dpmm = a4_dpi * 0.0394

def save_image(filename: str, image: MatLike, dpi: int):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    image_pil.save(filename, dpi=(dpi, dpi))


def marker_patch_size(size: int) -> Size:
    return (round(size * 1.2), round(size * 1.2 + 25))


def place_marker(image: MatLike, marker: Marker, size: int, point: Point):
    marker_gray = cv2.aruco.generateImageMarker(MARKER_DICT, marker.value, sidePixels=size)
    marker = cv2.cvtColor(marker_gray, cv2.COLOR_GRAY2BGR)
    
    h, w = marker.shape[:2]
    x, y = point

    image[y:y+h, x:x+w] = marker


def main():
    charuco_size: Size = (7, 5)
    charuco_margin = round(15 * a4_dpmm)
    charuco_board = cv2.aruco.CharucoBoard(size=charuco_size, squareLength=1, markerLength=0.8, dictionary=MARKER_DICT)
    charuco_image = charuco_board.generateImage(outSize=a4_size, marginSize=charuco_margin)

    save_image("out/charuco.png", charuco_image, a4_dpi)


    marker_image = np.full((a4_size[1], a4_size[0], 3), 255, dtype=np.uint8)
    marker_size = round(10 * a4_dpmm)
    marker1 = cv2.aruco.generateImageMarker(MARKER_DICT, Marker.THUMB.value, sidePixels=marker_size)
    marker1 = cv2.cvtColor(marker1, cv2.COLOR_GRAY2BGR)
    h, w = marker1.shape[:2]

    x, y = 20, 20

    marker_image[y:y+h, x:x+w] = marker1

    cv2.putText(marker_image, "Thumb", (x, y+h+25), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


    



    save_image("out/markers.png", marker_image, a4_dpi)

    return

    size = 250
    marker1 = cv2.aruco.generateImageMarker(MARKER_DICT, Marker.THUMB.value, sidePixels=size)
    border_thickness = size // 6
    white = (255, 255, 255)
    marker1 = cv2.copyMakeBorder(marker1, border_thickness, border_thickness, border_thickness, border_thickness, borderType=cv2.BORDER_CONSTANT, value=white)
    cv2.putText(marker1, 'OpenCV', ((size + border_thickness * 2)//2, size + border_thickness * 2 - 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA, bottomLeftOrigin=False)
    cv2.imshow("TEST", marker1)
    cv2.waitKey(2)

    # cv2.aruco.CharucoBoard().generateImage
    # 

    input()


if __name__ == "__main__":
    main()