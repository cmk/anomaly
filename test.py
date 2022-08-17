from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
import libcamera
import numpy as np

# import cv2 as cv2
from PIL import Image, GifImagePlugin

# TODO
#  - use EventHandlers and callbacks to draw gifs
#  - run camera feed without X-windows
#  - adjust exposure time to time of day

GifImagePlugin.LOADING_STRATEGY = 2

picam2 = Picamera2()

# camera_config = picam2.create_preview_configuration()
# picam2.configure(camera_config)
# picam2.start_preview(Preview.QTGL)
# picam2.start()
# time.sleep(2)
# picam2.capture_file("test.jpg")

config = picam2.create_preview_configuration(main={"size": (1920,1080)})
config["transform"] = libcamera.Transform(hflip=1)

picam2.configure(config)
#encoder = H264Encoder(repeat=True, iperiod=15)

picam2.start_preview(Preview.QTGL, width=1920,height=1080)
picam2.start()

#picam2.configure("preview")
#picam2.start(show_preview=True)


#overlay[:150, 200:] = (255, 0, 0, 64) # reddish
#overlay[150:, :200] = (0, 255, 0, 64) # greenish
#overlay[150:, 200:] = (0, 0, 255, 64) # blueish

width = 1920
height = 1080
blank = np.zeros((height, width, 4), dtype=np.uint8)
blank[:,:] = (0,0,0,0)

# Load the arbitrarily sized image
src1 = Image.open('gifs/A1.gif')
#src2 = Image.open('gifs/a2.gif')
src3 = Image.open('gifs/A3.gif')

# mask = Image.open('mask.png')


def playFrame(src, start=0):
    
    # Create an image padded to the required size with mode 'RGB'
    pad = Image.new('RGBA', (1920, 1080))
#         ((src.size[0] + width-1) // width) * width,
#         ((src.size[1] + height-1) // height) * height,
#         ))

    frameIdx = src.tell()
    if frameIdx >= src.n_frames-1:
        src.seek(start)
        frameIdx = start

    pad.paste(src) #, (0, 0, 540, 540))
    picam2.set_overlay(np.array(pad))
    
    src.seek(frameIdx+1)


def playGif(src, loops=1, intro=20):
    
    
   for i in range(0, min(intro, src.n_frames)):
       playFrame(src)
       
        
   picam2.set_overlay(blank) 

        
        
        ## pad.alpha_composite(src)
        # Paste the original image into the padded one

    
#src.info['transparency'] = 255
#src.info['background'] = 0
#src.convert('RGBA')

#pad.paste(src) #, (0, 0, 540, 540))
#picam2.set_overlay(np.array(pad))
#overlay = picam2.set_overlay(np.array(mask))
#overlay.window = (0, 0, 400, 400)


#     
# # By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the preview
# o.alpha = 255
# o.layer = 3

# overlay = cv2.im

#     
# # By default, the overlay is in layer 0, beneath the
# preview (which defaults to layer 2). Here we make
# the new overlay semi-transparent, then move it above
# the previewread("kitten.gif", cv2.IMREAD_UNCHANGED)
# picam2.set_overlay(overlay)