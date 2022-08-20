#!/usr/bin/python3

from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
# import libcamera as lc
import numpy as np
import serial as sp
import random as rng

# import cv2 as cv2
from PIL import Image, GifImagePlugin

path = '/home/cmk/Documents/anomaly/gifs/'
GifImagePlugin.LOADING_STRATEGY = 2

#width = 1920
#height = 1080

width = 1920 // 8
height = 1080 // 8

# Load the images
intro = Image.open(path + 'intro.gif')
src1 = Image.open(path + 'A1.gif')
src2 = Image.open(path + 'A2.gif')
#src3 = Image.open('gifs/A3.gif')

# mask = Image.open('mask.png')

# TODO
#  - use EventHandlers and callbacks to draw gifs
#  - run camera feed without X11?
#  - ensure exposure is auto adjusted, else adjust exposure time to time of day

# Sleep to allow X11 to finish booting
# time.sleep(20)

rng.seed()
compass = sp.Serial(port = "/dev/ttyACM0", baudrate=9600, bytesize=8, timeout=2)
# serialPort.open()


picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (width,height)})
#config["transform"] = libcamera.Transform(hflip=1) #dont need

picam2.configure(config)
#encoder = H264Encoder(repeat=True, iperiod=15)
#with picam2.constrols as ctl:
#    ctl.ExposureTime
picam2.start_preview(Preview.QTGL, width=width,height=height)
picam2.start()

#picam2.configure("preview")
#picam2.stfart(show_preview=True)


# blank = np.zeros((height, width, 4), dtype=np.uint8)
# blank[:,:] = (0,0,0,0)
# blank[500:, :500] = (255, 0, 0, 128)
# picam2.set_overlay(blank)



def playFrame(src, start=0):
    
    # Create an image padded to the required size with mode 'RGB'
    pad = Image.new('RGBA', (width, height))
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


def playGif(src, loops=1, intro=0):
    
    for i in range(0, max(intro, src.n_frames)):
        playFrame(src)
       
    picam2.set_overlay(None) 

def playSeq(src, intro, loops=1):
    
    playGif(intro, 1)
    playGif(src, loops)

def getHeading(port):
    
    try:
        raw = port.readline().rstrip()
        return int(raw[0:4].decode("utf-8"))
    
    except:
        return 60 # 2 o'clock

def close(h1, h2, tol=20):
    
    return abs(h1 - h2) < tol

def maybe(default, x):
    
    try: x
        
    except: default
        
lower = 320
upper = lower + 100
trigger = 0

while 1:
    
    if(compass.in_waiting > 0):
        
        time.sleep(0.1)
        heading = getHeading(compass)
        print(heading)
        
        if close(trigger, heading):
            
            print("Playing Gif sequence")
            playSeq(src2, intro, 4)
            trigger = rng.randint(lower, upper) % 360
            print("new trigger")
            print(trigger)
            print("done")
            
        
        
# playFrame(src1)
# time.sleep(60)
# 
            
        
