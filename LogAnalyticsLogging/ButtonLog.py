# Send log on button press
# This script requires the neccecary variables be configured in LogAnalyticsLogging/LALog.py
# This is an uncomplicated script that serves one purpose: Sending a log to a log analytics workspace when a button is pressed.

import threading
import time
from LALog import *

# GPIO settings
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# GPIO pin setup
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(7, GPIO.OUT)
GPIO.setwarnings(False)

def ledOn():
    GPIO.output(7, GPIO.HIGH)

def ledOff():
    GPIO.output(7, GPIO.LOW)

def listenForButton():
	while 1:
		time.sleep(0.5)
		if GPIO.input(11):
			# Button Press
            # I was experimenting with threading here. The threading isn't neccecary, just some experimentation
			x = threading.Thread(target=ledOn)
			x.start()
			z = threading.Thread(target=send_log, args=('IOLog','Action','Button Pressed'))
			z.start()
			time.sleep(1.3)
			y = threading.Thread(target=ledOff)
			y.start()

listenForButton()
