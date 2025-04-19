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
    return (round(size * 1.2), round(size * 1.2 + 30))


def place_marker(image: MatLike, marker: Marker, size: int, point: Point):
    marker_gray = cv2.aruco.generateImageMarker(MARKER_DICT, marker.marker_id, sidePixels=size)
    marker_image = cv2.cvtColor(marker_gray, cv2.COLOR_GRAY2BGR)
    
    pw, ph = marker_patch_size(size)

    h, w = marker_image.shape[:2]
    x, y = point

    wo, ho = (pw - w) // 2, (ph - h) // 2

    image[ho+y:ho+y+h, wo+x:wo+x+w] = marker_image

    cv2.rectangle(image, point, (x+pw, y+ph), (20, 20, 20), 2)
    cv2.putText(image, marker.display_name, (wo+x, ho+y+h+20), cv2.QT_FONT_NORMAL, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def main():
    generate_charuco_image()
    generate_marker_image()

def generate_charuco_image():
    size: Size = (7, 5)
    margin = round(15 * a4_dpmm)

    charuco_board = cv2.aruco.CharucoBoard(size=size, squareLength=1, markerLength=0.8, dictionary=MARKER_DICT)
    charuco_image = charuco_board.generateImage(outSize=a4_size, marginSize=margin)

    save_image("out/charuco.png", charuco_image, a4_dpi)


def generate_marker_image():
    margin = round(15 * a4_dpmm)
    duplicates = 7

    marker_image = np.full((a4_size[1], a4_size[0], 3), 255, dtype=np.uint8)
    marker_size = round(10 * a4_dpmm)
    
    pw, ph = marker_patch_size(marker_size)
    wo, ho = pw + round(3 * a4_dpmm), ph + round(3 * a4_dpmm)

    for i, marker in enumerate(Marker):
        for j in range(duplicates):
            place_marker(marker_image, marker, marker_size, (margin+i*wo, margin+j*ho))

    save_image("out/markers.png", marker_image, a4_dpi)


if __name__ == "__main__":
    main()