import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time


camera = PiCamera()
camera.resolution = (1296,736)
camera.framerate=30
rawCapture = PiRGBArray(camera, size=(1296,736))

# Need to allow the camera to initilize 
time.sleep(0.1)

def face_detected(image):
	if image is not None:
		return True
	else:
		return False

def detected_person():
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		person = False
		# Define the Facial Recognition
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(gray,1.3,5)
		
		for (x,y,w,h) in faces:
			r = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = image[y:y+h, x:x+w]
			person = face_detected(r)
	
		#cv2.imshow('Feed', image)
		#key = cv2.waitKey(10) & 0xFF

		#rawCapture.truncate(0)
		#print(person)
		return person
		'''if key == ord("q"):
			break'''
		


print(detected_person())
	

