#!/usr/bin/python3

import keyboard
import time
import sys

sys.path.insert(1, '/home/cmk/Documents/picamera2')

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
# import libcamera as lc
import numpy as np
import serial as sp
import random as gn

# import cv2 as cv2
from PIL import Image, GifImagePlugin

# Gif constants
path = '/home/cmk/Documents/anomaly/gifs/'
GifImagePlugin.LOADING_STRATEGY = 2

# Image constants
redux = 2
pixw = 1920 # width * redux
pixh = 1080 # height * redux
width = pixw // redux
height = pixh // redux
center = (width//2,height//2)
hires = {"size": (pixw,pixh)}
lores = {"size": (width,height), "format": "YUV420"}

# Compass variables        
fovmax = 360 # field of view
offset = 0
margin = 30
trigger = 0

# Load the images
intro = Image.open(path + 'intro.gif')
gifs = []

for i in range(1, 3):
    gif = Image.open(path + 'A' + str(i) + '.gif')
    gifs.append(gif)

# mask = Image.open('mask.png')

# TODO
#  - run camera feed without X11?
#  - ensure exposure is auto adjusted, else adjust exposure time to time of day
#  - use server / EventHandlers and callbacks to draw gifs
#    python should only process/insert images when triggered: picam2.post_callback = playFrame ?

# Sleep to allow X11 to finish booting
# time.sleep(20)


gn.seed()
compass = sp.Serial(port = "/dev/ttyACM0", baudrate=9600, bytesize=8, timeout=2)
# serialPort.open()


picam2 = Picamera2()
config = picam2.create_preview_configuration(main=lores)
#config["transform"] = libcamera.Transform(hflip=1) #dont need

picam2.configure(config)
#encoder = H264Encoder(repeat=True, iperiod=15)
#with picam2.constrols as ctl:
#    ctl.ExposureTime
# picam2.start_preview(Preview.DRM, x=pixw, y=pixh, width=pixw, height=pixh)
picam2.start_preview(Preview.DRM, width=width, height=height)
picam2.start()

#picam2.configure("preview")
#picam2.stfart(show_preview=True)


# blank = np.zeros((height, width, 4), dtype=np.uint8)
# blank[:,:] = (0,0,0,0)
# blank[500:, :500] = (255, 0, 0, 128)
# picam2.set_overlay(blank)


    
def window(phi):

    return min(fovmax, abs(phi))

def travel(phi):

    midpoint = fovmax // 2

    if phi > midpoint:
        return gn.randint(0, midpoint - margin)

    return gn.randint(midpoint + margin, fovmax)

def getHeading(port):
    
    try:
        raw = port.readline().rstrip()
        return int(raw[0:4].decode("utf-8")) + offset
    
    except:
        return fovmax // 2 # center of view

def close(h1, h2):
    
    return abs(h1 - h2) < margin

def playFrame(gif):
    
    # Create an image padded to the required size with mode 'RGB'
    pad = Image.new('RGBA', (width, height))
    # pad = Image.new('RGBA', (500, 500))
#         ((gif.size[0] + width-1) // width) * width,
#         ((gif.size[1] + height-1) // height) * height,
#         ))

    frameIdx = gif.tell()
    if frameIdx >= gif.n_frames-1:
        frameIdx = 0
        gif.seek(frameIdx)

    # pad.paste(gif, center)
    pad.paste(gif)
    picam2.set_overlay(np.array(pad))
    
    gif.seek(frameIdx+1)


def playGif(gif, loops=1):
    
    for i in range(0, max(0, gif.n_frames)):
        playFrame(gif)
       
    picam2.set_overlay(None) 

def playSeq(gif, intro, loops=1):
    
    playGif(intro, 1)
    playGif(gif, loops)


while 1:

    if (keyboard.is_pressed('q')):
        sys.exit()
     
    if(compass.in_waiting > 0):
         
        # time.sleep(0.1)
        heading = getHeading(compass)
        print(heading)
        
        if close(trigger, heading):
            
            print("Playing Gif sequence")
            gif = gn.choice(gifs)
            playSeq(gif, intro, 1)
            trigger = travel(heading)
            print("new trigger")
            print(trigger)
            print("done")
        
# time.sleep(60)
# 
            
        
