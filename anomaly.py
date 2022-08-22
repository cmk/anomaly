#!/usr/bin/python3

import keyboard
import time
import sys

# sys.path.insert(1, '/home/cmk/Documents/picamera2')

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
redux = 12
pixw = 1728 # camw * redux
pixh = 972 # camh * redux
camw = pixw // redux
camh = pixh // redux
center = (pixw//2 - 250,pixh//2 - 250)
hires = {"size": (pixw,pixh)}
lores = {"size": (camw,camh), "format": "YUV420"}

# Compass variables        
offset = 0
fovmax = 360 # field of view
midpoint = offset + fovmax // 2
margin = 90
trigger = 0

# Load the images
intro = Image.open(path + 'intro.gif')
gifs = []

for i in range(0, 33):
    gif = Image.open(path + 'A' + str(i) + '.gif')
    gifs.append(gif)

# mask = Image.open('mask.png')

# TODO
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

picam2.configure(config)
# picam2.start_preview(Preview.DRM, width=pixw, height=pixh)
# picam2.start_preview(Preview.QTGL, width=pixw, height=pixh)
picam2.start_preview(Preview.QTGL, width=1920, height=1080)
picam2.start()

#picam2.configure("preview")
#picam2.stfart(show_preview=True)


# blank = np.zeros((camh, camw, 4), dtype=np.uint8)
# blank[:,:] = (0,0,0,0)
# blank[500:, :500] = (255, 0, 0, 128)
# picam2.set_overlay(blank)


    
def window(phi):

    return min(fovmax, abs(phi))

def travel(phi):

    if phi > midpoint:
        return gn.randint(0, midpoint - margin)

    return gn.randint(midpoint + margin, fovmax)

def getHeading(port):
    
    try:
        raw = port.readline().rstrip()
        return int(raw[0:4].decode("utf-8")) + offset
    
    except:
        return midpoint

def close(h1, h2):
    
    return abs(h1 - h2) < margin

def playFrame(gif, loc=center):
    
    # Create an image padded to the required size with mode 'RGB'
    pad = Image.new('RGBA', (pixw, pixh))
    frameIdx = gif.tell()
    
    if frameIdx >= gif.n_frames-1:
        frameIdx = 0
        gif.seek(frameIdx)

    pad.paste(gif, loc)
    picam2.set_overlay(np.array(pad))
    gif.seek(frameIdx+1)


def playGif(gif, loops=1, loc=center):
    
    for i in range(0, max(10, gif.n_frames)):
        playFrame(gif)
       
    picam2.set_overlay(None) 

def playSeq(gif, intro, loops=1):
    
    loc = (pixw//2 - 250 + gn.randint(-40, 40),pixh//2 - 250 + gn.randint(-20, 20))
    playGif(intro, 1, loc)
    playGif(gif, loops, loc)

# time.sleep(5)
# gif = gn.choice(gifs)
# playFrame(intro)
# playSeq(gif, intro, 1)
# sys.exit()
 
while 1:

    if (keyboard.is_pressed('q')):
        sys.exit()
     
    if(compass.in_waiting > 0):
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
