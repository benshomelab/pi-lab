# The benshomelab pi-lab repo
This repository contains projects completed using a Raspberry PI 3 Model B

# Contents
[E-Paper project](e-paper) | Python project that pulls data from a variety of sources and displays it on an e-paper display.

[LogAnalyticsLogging](LogAnalyticsLogging) | Experimentation with submitting logs via python to an Azure log Analytics Workspace

[motionAlert](motionAlert) | Trigger an Azure Logic App based on the PI's GPIO input monitoring using Python

## E-Paper project details

### Hardware

E-Paper display - [7.5inch E-Paper E-Ink Display HAT (B) For Raspberry Pi, 800×480, Red / Black / White, SPI](https://www.waveshare.com/7.5inch-e-Paper-HAT-B.htm)

### Documentation/Dependancies/Examples from Waveshare

Waveshare's documentation regarding how to setup a Raspberry PI for displaying onto the e-paper display. These instructions include installing depandancies, enabling the SPI interface, and links to their demo codes. [Raspberry Pi Guides for SPI e-Paper](https://www.waveshare.com/wiki/Template:Raspberry_Pi_Guides_for_SPI_e-Paper)

### My e-paper python code

High level design of my project is the following:

1. Systemd is what handles the running of the python scripts. Systemd allows for running the python scripts as a service, which provides handling of script crashes and easy monitoring of the service using systemctl and journalctl.

    For reference, the systemd service I created has a config file like the following:
    ```
    [Unit]
    Description=Drives e-paper display
    After=multi-user.target
    [Service]
    Type=simple
    Restart=always
    RestartSec=60
    ExecStart=/usr/bin/python3 <path to e-paper handler script>
    [Install]
    WantedBy=multi-user.target
    ```
    
    This file should be named `<your-service-name>.service` and should be placed in the /etc/systemd/system/ directory.
    
    Once the file exists there, you will need to run the follwing commands:
    `sudo systemctl daemon-reload`
    
    `sudo systemctl enable <your-service-name>.service`
    
    `sudo systemctl start <your-service-name>.service`
    
    The following Journalctl command can be used to monitor the service/python script output 
    
    `sudo journalctl -f -u <your-service-name>.service`

2. The main python script is [e-paper-handler.py](e-paper/e-paper-handler.py). This script imports modules from all other scripts used.
3. [e-paper-handler.py](e-paper/e-paper-handler.py) uses a while loop to update the e-paper screen every sixty seconds only if there is a change in the data to be displayed. Currently, I have implemented:

    - [birthdayCheck.py](e-paper/birthdayCheck.py) - Provides a list of all birthdays that take place in the next month based on the data it retrieves from [birthdays.txt](e-paper/birthdays.txt).
    - [azureGets.py](e-paper/azureGets.py) - Provides API calls that retrieve data from my Azure lab. Currently, the following are implemented:
        - `getVmStatus()` - Retrieves the powerstate of an Azure VM using the following API call - [Virtual Machines - Instance View](https://learn.microsoft.com/en-us/rest/api/compute/virtual-machines/instance-view?tabs=HTTP)
        - `getBudget()` - Retrieves the current cost per a Budget of my Azure subscription using the following API call - [Budgets - Get](https://learn.microsoft.com/en-us/rest/api/consumption/budgets/get?tabs=HTTP)
        - `getCalendarEvents()` Retrieves all calendar events on a specified user's calendar happening on the current day using the following API call (This has code for adjusting timezone from UTC to EST) - [Get event](https://learn.microsoft.com/en-us/graph/api/event-get?view=graph-rest-1.0&tabs=http)
