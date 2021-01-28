#!/usr/bin/env python3

from LYWSD03MMC_handler import LYWSD03MMC_reader
from LYWSDCGQ_handler import LYWSDCGQ_reader
from SimpleLogger import SimpleLogger

import time

'''
MAC Addresses:
'58:2D:34:38:3C:E2' - LYWSDCGQ  
'A4:C1:38:EA:1D:CC' - LYWSD03MMC kitchen  
'A4:C1:38:5B:10:E2' - LYWSD03MMC outside  
'A4:C1:38:D2:7A:00' - LYWSD03MMC filament  
'''
logger = SimpleLogger(verbose = True, loggerName = f"Xiaomi sensors")

sensor1 = LYWSD03MMC_reader('A4:C1:38:EA:1D:CC', "kitchen")
sensor2 = LYWSD03MMC_reader('A4:C1:38:5B:10:E2', "outside")
sensor3 = LYWSD03MMC_reader('A4:C1:38:D2:7A:00', "filament")
sensor4 = LYWSDCGQ_reader('58:2D:34:38:3C:E2', "bathroom")

while 1:
    ret = sensor1.read_data()
    if ret is not None:
        logger.log(f"Data from {sensor1.name} ({sensor1.mac}): {ret}")
    else:
        logger.log(f"Empty data from {sensor1.name} ({sensor1.mac})", messageType = "WARN", forcePrint = True)

    ret = sensor2.read_data()
    if ret is not None:
        logger.log(f"Data from {sensor2.name} ({sensor2.mac}): {ret}")
    else:
        logger.log(f"Empty data from {sensor2.name} ({sensor2.mac})", messageType = "WARN", forcePrint = True)

    ret = sensor3.read_data()
    if ret is not None:
        logger.log(f"Data from {sensor3.name} ({sensor3.mac}): {ret}")
    else:
        logger.log(f"Empty data from {sensor3.name} ({sensor3.mac})", messageType = "WARN", forcePrint = True)

    ret = sensor4.read_data()
    if ret is not None:
        logger.log(f"Data from {sensor4.name} ({sensor4.mac}): {ret}")
    else:
        logger.log(f"Empty data from {sensor4.name} ({sensor4.mac})", messageType = "WARN", forcePrint = True)


