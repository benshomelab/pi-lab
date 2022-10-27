#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
from datetime import datetime
from azureGets import *
from birthdayCheck import *
import logging
logging.basicConfig(level=logging.DEBUG)


picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in5b_V2
import time
from PIL import Image,ImageDraw,ImageFont

# Variables for data organization
bdayStartIndexY = 120
bdayListIndexY = bdayStartIndexY + 27
calendarEventsStartIndexY = 220
calendarEventsListIndexY = bdayStartIndexY + 27

# e-paper dependancies initialization
epd = epd7in5b_V2.EPD()
epd.init()

try:
    # Fonts
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # Variables used for tracking any changes in retrieved data
    storedStat = "cowabunga"
    storedBudget = 1000000
    storedBdays = []
    storedTime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    storedCalendarEvents = ['bing bong mofo']
    while(1):
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        Other = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw_Himage = ImageDraw.Draw(Himage)
        draw_other = ImageDraw.Draw(Other)

        # getting and drawing azure VM status
        curStat = getVmStatus()
        if(curStat == "VM running"):
            draw_Himage.text((10, 20), 'Azure VM running', font = font24, fill = 0)
        elif(curStat == "VM deallocated"):
            draw_Himage.text((10, 20), 'Azure VM offline', font = font24, fill = 0)
        else:
            draw_Himage.text((10, 20), 'Azure VM transitioning', font = font24, fill = 0)

        # Getting and drawing Azure subscription budget current cost
        curBudget = getBudget()
        draw_Himage.text((10, 45), 'Current Azure subcription cost: $' + str(curBudget), font = font18, fill = 0)

        # Getting and drawing birthday data
        bs = birthdaysSoon()
        bdayListIndexY = bdayStartIndexY + 27
        draw_Himage.text((10, bdayStartIndexY), "Upcoming Birthdays", font = font24, fill = 0)
        for person in bs:
            draw_Himage.text((10, bdayListIndexY), person, font = font18, fill = 0)
            bdayListIndexY += 22

        # Getting and drawing calendar events
        calendarEvents = getCalendarEvents()
        calendarEventsListIndexY = calendarEventsStartIndexY + 27
        draw_Himage.text((10, calendarEventsStartIndexY), "Calendar Events", font = font24, fill = 0)

        for event in calendarEvents:
            draw_Himage.text((10, calendarEventsListIndexY), event, font = font18, fill = 0)
            calendarEventsListIndexY += 22

        # Only updating screen if something has changed
        if(storedStat != curStat or storedBudget != curBudget or bs != storedBdays or storedCalendarEvents != calendarEvents):
            logging.info('Changes found, writing to screen then waiting 60 seconds')
            epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))
            storedStat = curStat
            storedBudget = curBudget
            storedBdays = bs
            storedCalendarEvents = calendarEvents
        else:
            logging.info('No change detected, waiting 60 seconds then looping')
        time.sleep(60)

# Handing errors
except IOError as e:
    logging.info(e)
# Handling keyboard interrupt
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit()
    exit()
