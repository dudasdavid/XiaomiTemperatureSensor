#!/usr/bin/env python3

from LYWSD03MMC_handler import LYWSD03MMC_reader
from LYWSDCGQ_handler import LYWSDCGQ_reader
from SimpleLogger import SimpleLogger

import time
import subprocess

if __name__ == "__main__":
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
        while 1:
            ret = sensor1.read_data()
            if ret is not None:
                logger.log(f"Data from {sensor1.name} ({sensor1.mac}): {ret}")
                sensor1JSON=f'{sensor1.name}-temperature={ret["temperature"]}&{sensor1.name}-humidity={ret["humidity"]}&{sensor1.name}-battery={ret["battery"]}'
                break
            else:
                logger.log(f"Empty data from {sensor1.name} ({sensor1.mac}), retrying...", messageType = "WARN")

        while 1:
            ret = sensor2.read_data()
            if ret is not None:
                logger.log(f"Data from {sensor2.name} ({sensor2.mac}): {ret}")
                sensor2JSON=f'{sensor2.name}-temperature={ret["temperature"]}&{sensor2.name}-humidity={ret["humidity"]}&{sensor2.name}-battery={ret["battery"]}'
                break
            else:
                logger.log(f"Empty data from {sensor2.name} ({sensor2.mac}), retrying...", messageType = "WARN")

        while 1:
            ret = sensor3.read_data()
            if ret is not None:
                logger.log(f"Data from {sensor3.name} ({sensor3.mac}): {ret}")
                sensor3JSON=f'{sensor3.name}-temperature={ret["temperature"]}&{sensor3.name}-humidity={ret["humidity"]}&{sensor3.name}-battery={ret["battery"]}'
                break
            else:
                logger.log(f"Empty data from {sensor3.name} ({sensor3.mac}), retrying...", messageType = "WARN")

        while 1:
            ret = sensor4.read_data()
            if ret is not None:
                logger.log(f"Data from {sensor4.name} ({sensor4.mac}): {ret}")
                sensor4JSON=f'{sensor4.name}-temperature={ret["temperature"]}&{sensor4.name}-humidity={ret["humidity"]}&{sensor4.name}-battery={ret["battery"]}'
                break
            else:
                logger.log(f"Empty data from {sensor4.name} ({sensor4.mac}), retrying...", messageType = "WARN")


        upload_data = f"{sensor1JSON}&{sensor2JSON}&{sensor3JSON}&{sensor4JSON}"

        subprocess.call(["bash", "./send_data.bash", upload_data])
