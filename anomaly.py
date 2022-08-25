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
# import struct as st

# import cv2 as cv2
from PIL import Image, GifImagePlugin

# mask = Image.open('mask.png')

# TODO
#  - ensure exposure is auto adjusted, else adjust exposure time to time of day
#  - use server / EventHandlers and callbacks to draw gifs
#    python should only process/insert images when triggered: picam2.post_callback = playFrame ?

# Gif constants
path = '/home/cmk/Documents/anomaly/gifs/'
GifImagePlugin.LOADING_STRATEGY = 2

# Image constants
redux = 12
# pixh = 1728 # camw * redux
# pixw = 972 # camh * redux
# pixw = 1728 # camw * redux
# pixh = 972 # camh * redux
# pixh = 1920 # camw * redux
# pixw = 1080 # camh * redux
pixw = 1720 # camw * redux
pixh = 1080 # camh * redux
camw = pixw // redux
camh = pixh // redux
center = (pixw//2 - 250,pixh//2 - 250)
hires = {"size": (pixw,pixh)}
lores = {"size": (camw,camh), "format": "YUV420"}

# Compass variables        
offset = 0
fovmax = 180 # field of view
margin = 30
triggers = [offset]

# Load the images
intro = Image.open(path + 'intro.gif')
gifs = []

for i in range(0, 31):
    gif = Image.open(path + 'A' + str(i) + '.gif')
    gifs.append(gif)

# Sleep to allow X11 to finish booting
time.sleep(10)


gn.seed()
    
picam2 = Picamera2()
config = picam2.create_preview_configuration(main=lores)

picam2.configure(config)
# picam2.start_preview(Preview.DRM, width=pixw, height=pixh)
picam2.start_preview(Preview.QTGL, x=200, width=pixw, height=pixh)
# picam2.start_preview(Preview.QTGL, width=1920, height=1080)
picam2.start()

    
def generate(maximum, offset=0):

    return (gn.randint(0, 1000000) % maximum) + offset


def getHeading(port):
   
    raw = port.readline().rstrip()
    val =int(raw.decode("utf-8"))
    # proc = window(raw[0:2].decode("utf-8"))
    # proc = st.unpack('<h', raw[0:2])
    port.reset_input_buffer()
    return min(val, fovmax) + offset


def close(h1, h2):
   
    w1 = min(h1, fovmax)
    w2 = min(h2, fovmax)
    return abs(w1 - w2) < margin

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


def playGif(gif, loc=center):
    
    for i in range(0, max(10, gif.n_frames)):
        playFrame(gif)
       
    picam2.set_overlay(None) 

def playSeq(gif, loc=center):
    
    playGif(intro, loc)
    playGif(gif, loc)

def anomaly(heading):

    trigger = triggers[0]
    if close(trigger, heading):
        print(f"You found an anomaly! The heading was {trigger}.")
        print(trigger)
        gif = gn.choice(gifs)
        loc = (pixw//2 - generate(pixw//2, -200), pixh//2 - generate(pixw//2, -200))
        playSeq(gif, loc)
        
        while close(triggers[0], heading):
            triggers.pop()
            next_trigger = generate(fovmax, offset)
            triggers.append(next_trigger)
        
        print(f"The next trigger heading is {next_trigger}.")
        # print("new trigger")
        # print(trig)
        # print("done")

def fallback():

    gif = gn.choice(gifs)
    loc = (generate(pixw), generate(pixh))
    playSeq(gif, loc)
    period = gn.randint(20, 35)
    time.sleep(period)


try:
    try:
        compass = sp.Serial(port = "/dev/ttyACM0", baudrate=9600, parity=sp.PARITY_NONE, bytesize=sp.EIGHTBITS, timeout=0.1)
        compass.readline()

    except BaseException as err:
        print(f"168: Unexpected {err=}, {type(err)=}")
        compass = sp.Serial(port = "/dev/ttyACM1", baudrate=9600, parity=sp.PARITY_NONE, bytesize=sp.EIGHTBITS, timeout=0.1)
        compass.readline()

except BaseException as err:
    print(f"173: Unexpected {err=}, {type(err)=}")
    fallback()
 
while 1:

    if (keyboard.is_pressed('q')):
        sys.exit()
    
    if compass.in_waiting > 0:
        try:
            heading = getHeading(compass)
            print(heading)
            anomaly(heading) 

        except BaseException as err:
            print(f"184: Unexpected {err=}, {type(err)=}")
            if (keyboard.is_pressed('q')):
                sys.exit()
            fallback()
