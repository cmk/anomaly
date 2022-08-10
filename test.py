from picamera2 import Picamera2, Preview
import time
import numpy as np
# import cv2 as cv2
from PIL import Image

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

width = 256
height = 128

# Load the arbitrarily sized image
img = Image.open('kitten2.gif')
# Create an image padded to the required size with
# mode 'RGB'
pad = Image.new('RGBA', (
    ((img.size[0] + width-1) // width) * width,
    ((img.size[1] + height-1) // height) * height,
    ))
# Paste the original image into the padded one
pad.paste(img, (0, 0))

# Add the overlay with the padded image as the source,
# but the original image's dimensions
picam2.set_overlay(np.array(pad))
# By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
# o.alpha = 255
# o.layer = 3

# overlay = cv2.imread("kitten.gif", cv2.IMREAD_UNCHANGED)
# picam2.set_overlay(overlay)