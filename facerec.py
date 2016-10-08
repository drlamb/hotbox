import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
from PIL import Image
#from bob.ip.base.Flandmark import Flandmark


camera = PiCamera()
camera.resolution = (1296,736)
rawCapture = PiRGBArray(camera, size=(1296,736))

# Need to allow the camera to initilize 
time.sleep(0.1)

# Returns True if a rectangle was made on the image.
def face_detected(image):
	return True if image is not None else False

def detected_person():

	filters = ['eye.xml', 'full_frontal.xml', 'profile.xml', 'profile_flipped.xml', 'eye_rotated.xml', 'eye_rotated2.xml', 'eye_rotated3.xml', 'eye_rotated4.xml']]
	for file in filters:
		
		if file == "profile_flipped.xml":
			camera.hflip = True
		if file == 'eye_rotated.xml':
			camera.rotation = 90
		if file == 'eye_rotated2.xml':
			camera.rotation = 270
		

		camera.capture('image.jpg')
		pil_image = Image.open('image.jpg').convert('RGB')
		open_cv_image = np.array(pil_image)
		open_cv_image = open_cv_image[:, :, ::-1].copy()
		person = False
		# Define the Facial Recognition
		gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
		print file
		face_cascade = cv2.CascadeClassifier(file)
		faces = face_cascade.detectMultiScale(gray,1.3,5)
	
		for (x,y,w,h) in faces:
			r = cv2.rectangle(open_cv_image,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = open_cv_image[y:y+h, x:x+w]
			person = face_detected(r)
			print person
		camera.rotation = 0
		camera.hflip = False
	print "Finished loop"
	#return person
	
detected_person()
	

