# This script sends a log of the speed test results to log analytics

import speedtest
from LALog import *
import time

# Logging config
newYorkTz = pytz.timezone("America/New_York")

def startSpeedtest():
	s = speedtest.Speedtest()
	s.get_best_server()
	s.download()
	s.upload()
	s.results.share()
	results_dict = s.results.dict()
	dSpeed = results_dict['download'] / 1048576
	uSpeed = results_dict['upload'] / 1048576
	send_log('SpeedTest','Result', 'Upload:' + str(uSpeed) + ',Download:' + str(dSpeed))

while True:
	try:
		startSpeedtest()
	except:
		print('Something went wrong with speedtest')
	time.sleep(90) # 900 for 15 mins
