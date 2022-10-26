# The purpose of this script is to trigger an Azure logic app when a motion detector is triggered

import requests
import time
from datetime import datetime
import RPi.GPIO as GPIO

def tell_azure():
	url = '<URL for Azure logic app to be triggered>'
	r =requests.put(url)
	print(r.status_code)

def getReading():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(5, GPIO.IN)
	while True:
		print(str(GPIO.input(5)))
		if(GPIO.input(5) == 1):
			print("Motion Detected, telling azure")
			tell_azure()
			time.sleep(30)
		time.sleep(3)

getReading()
