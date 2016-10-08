import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

camera = PiCamera()
camera.resolution = (1920,1080)
camera.framerate=30
rawCapture = PiRGBArray(camera, size=(1920,1080))

# Need to allow the camera to initilize 
time.sleep(0.1)


