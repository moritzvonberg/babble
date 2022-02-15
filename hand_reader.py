import pathlib
import logging
from time import time
from PIL.Image import Image as PILImage # used for type hint only
from win32 import win32gui
import numpy as np

from pytesseract.pytesseract import image_to_boxes, image_to_string
from PIL import Image, ImageDraw, ImageColor, ImageGrab

import pytesseract

pytesseract.pytesseract.tesseract_cmd = pathlib.WindowsPath('C:/Program Files/Tesseract-OCR/tesseract.exe')
custom_config = '''-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 10'''

tile_bg_color = (255, 246, 167)
tile_x_offset = 98

def get_window_image() -> PILImage:
    hwnd = win32gui.FindWindow(None, 'BabbleRoyale')
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        return [ImageGrab.grab(bbox=(803 + tile_x_offset * i , 1315, 866 + tile_x_offset * i, 1378)) for i in range(10)]
    else:
        logging.warn("couldn't find babble royale window to take screenshot")

t1 = time()        
# for i, image in enumerate(get_window_image()):
#     image.save(f"test_screenshots/{i}.png")

for i in range(10):
    with Image.open(f'test_screenshots/{i}.png') as image:
        #if tile background is bright enough
        if sum(image.getpixel((5,5))) > 600:
            print(image_to_string(image, config=custom_config))
            print(time() - t1)
        else:
            print(time() - t1)
            break
        

    # np_ary = np.array(image)
    # #split channels:
    # r, g, b = np.split(np_ary, 3, axis=2)
    # r=r.reshape(-1)
    # g=r.reshape(-1)
    # b=r.reshape(-1)
    # # Standard RGB to grayscale 
    # bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], 
    # zip(r,g,b)))
    # bitmap = np.array(bitmap).reshape([np_ary.shape[0], np_ary.shape[1]])
    # bitmap = np.dot((bitmap > 128).astype(float),255)
    # image = Image.fromarray(bitmap.astype(np.uint8))
    # print(image_to_string(image, config=custom_config))
    


# image_path = pathlib.WindowsPath('test_screenshots/cutout.png')
# print(pytesseract.image_to_string(str(image_path), config=custom_config))
# boxes = image_to_boxes(str(image_path))
# print(boxes)
# with Image.open(image_path) as image:
#     draw = ImageDraw.Draw(image)
#     red_color = ImageColor.getrgb('red')
#     for line in boxes.splitlines():
#         rectangle = tuple([int(x) for x in line.split(' ')[1:5]])
#         draw.rectangle(rectangle,outline=red_color)
#     image.show()


letter_module_top_left = (760, 1275)
letter_tiles = (793, 1305, 875, 1388)
letter_scan = (803, 1315, 866, 1378)
tile_x_offset = (100, 0, 100, 0)
hand_area = (803, 1315,1757, 1378)