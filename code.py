import RPi.GPIO as GPIO
from picamera import PiCamera
import pytesseract
from pytesseract import image_to_string 
from PIL import Image
import os,sys,time
import logging
import subprocess
from espeak import espeak
from subprocess import check_output
import codecs



camera  =  PiCamera ()
# Set the camera resolution to 512x512.
camera.resolution = (512,512)

# Set the GPIO pin configuration of RPi3 to BOARD mode.
# GPIO 16 --->  Triggers Camera capture.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

subprocess.check_output(['espeak','-vsw','KARIBU KATIKA MFUMO'])



def text_to_image(image):
    text = pytesseract.image_to_string(Image.open(image))
    file=codecs.open('file.txt', mode='w', encoding='utf8')
    file.write(text)
    print text

def espeak(text_file):
        f=open("file.txt", "r")
        fl =f.readlines()
        for x in fl:
            #print(x)
            speak=check_output(['espeak','-vsw',x])
                            
        
        
image =Image.open('image.jpg')
text_file=open('file.txt')
while True:
    try:
        # capture_button ---> Button input to capture new image.
        capture_button = GPIO.input(16)       

        #capture_button=0 -----> pressing capture button
        if  capture_button == False:
            time.sleep(1)
            #flag=0
            subprocess.check_output(['espeak','-vsw','MFUMO UNAPIGA PICHA'])

            # 2 second sleep to give sufficient time for the camera to initialize.
            camera.start_preview()
            time.sleep(2)
            camera.capture('image.jpg')
            
            subprocess.check_output(['espeak','-vsw','MFUMO UNAKAMILISHA'])           
            
           # camera()
            text_to_image('image.jpg')
            time.sleep(2)
            espeak('file.txt')    
    except Exception as e:
        print ( e )
        GPIO.cleanup()
        break
            
