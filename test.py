from picamera2 import Picamera2, Preview
import time
import numpy as np
# import cv2 as cv2
from PIL import Image, GifImagePlugin

GifImagePlugin.LOADING_STRATEGY = 2

picam2 = Picamera2()

# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")

picam2.configure(picam2.create_preview_configuration())
picam2.start(show_preview=True)
overlay = np.zeros((300, 400, 4), dtype=np.uint8)
overlay[:150, 200:] = (255, 0, 0, 64) # reddish
overlay[150:, :200] = (0, 255, 0, 64) # greenish
overlay[150:, 200:] = (0, 0, 255, 64) # blueish

width = 512
height = 256

# Load the arbitrarily sized image
src = Image.open('trans/donut_trans.gif')
src2 = Image.open('a2.gif')
src3 = Image.open('a3.gif')
# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGBA', (
    ((src.size[0] + width-1) // width) * width,
    ((src.size[1] + height-1) // height) * height,
    ))

src.info['transparency'] = 255
src.info['background'] = 0
src.convert('RGBA')

while 1:
    
    frameIdx = src.tell()

    # print(img.getbbox())
    if frameIdx >= src.n_frames-1:
        src.seek(0)
        frameIdx = 0
    
    
    ## pad.alpha_composite(src)
    # Paste the original image into the padded one
    pad.paste(src) #, (0, 0, 540, 540))
    picam2.set_overlay(np.array(pad))
    src.seek(frameIdx+1)
#     
# # By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
# o.alpha = 255
# o.layer = 3

# overlay = cv2.imread("kitten.gif", cv2.IMREAD_UNCHANGED)
# picam2.set_overlay(overlay)