# from types import CoroutineType
from picamera import PiCamera
import time
import cv2
from gpiozero import LED

camera=PiCamera()
camera.resolution=(1000,1000)
camera.brightness=44
camera.contrast=40


#camera.vflip=True
camera.start_preview()
time.sleep(1)
camera.capture("test1.jpeg")
img=cv2.imread("test1.jpeg")

croped_image= img[300:700,400:775]

# led = LED(17)
 
               

cv2.imwrite("final1.jpeg",croped_image)
# a=5

# while a==5:
    # led.on

