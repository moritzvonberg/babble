import pathlib
from win32 import win32gui
from PIL import Image, ImageDraw, ImageColor, ImageGrab
from PIL.Image import Image as PILImage # used for type hint only
import logging


def get_window_image() -> PILImage:
    hwnd = win32gui.FindWindow(None, 'BabbleRoyale')
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        return ImageGrab.grab(win32gui.GetWindowRect(hwnd))
    else:
        logging.warn("couldn't find babble royale window to take screenshot")
        
#TODO: Calculate hand position dynamically based on window size
letter_module_top_left = (760, 1275)
letter_tiles = (793, 1305, 875, 1388)
letter_scan = (803, 1315, 866, 1378)
tile_x_offset = 98

# image = get_window_image()

with ImageGrab.grab() as image:
    draw = ImageDraw.Draw(image)
    
    for i in range(10):
        pos = (803 + tile_x_offset * i , 1315, 866 + tile_x_offset * i, 1378)
        draw.rectangle(pos, outline=(255,0,0))
    image.save(pathlib.WindowsPath('test_screenshots/scanrects.png'))


def get_hand_images() -> list[PILImage]:
    return [Image.op]