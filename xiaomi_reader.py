#!/usr/bin/env python3

from LYWSD03MMC_handler import LYWSD03MMC_reader
from LYWSDCGQ_handler import LYWSDCGQ_reader
from SimpleLogger import SimpleLogger

import time
import os
import threading

import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime

def watchdog():
    watchdogLogger = SimpleLogger(verbose = True, loggerName = f"Watchdog")
    watchdogTimeout = 360 # 6 minutes timeout
    startTime = time.time()
    watchdogLogger.log(f"Watchdog started with {watchdogTimeout/60.0} minute timeout.", messageType = "DEBUG")
    while 1:
        if shutdownFlag.wait(timeout=1):
            break

        if time.time() - startTime > watchdogTimeout:
            watchdogLogger.log(f"Watchdog timeout expired! Force quitting the script!", messageType = "ERROR")
            #os.kill(0, 9) # stops the runner bash script :(
            os._exit(1)   

    watchdogLogger.log(f"Watchdog gracefully stopped after {(time.time() - startTime)/60.0} minute.", messageType = "DEBUG")

if __name__ == "__main__":
    '''
    MAC Addresses:
    '58:2D:34:38:3C:E2' - LYWSDCGQ  
    'A4:C1:38:EA:1D:CC' - LYWSD03MMC kitchen  
    'A4:C1:38:5B:10:E2' - LYWSD03MMC outside  
    'A4:C1:38:D2:7A:00' - LYWSD03MMC filament  
    '''
    logger = SimpleLogger(verbose = True, loggerName = f"Xiaomi sensors")

    shutdownFlag = threading.Event()
    watchdogThread = threading.Thread(target=watchdog, name="watchdog")
    watchdogThread.start()

    sensor1 = LYWSD03MMC_reader('A4:C1:38:EA:1D:CC', "kitchen")
    sensor2 = LYWSD03MMC_reader('A4:C1:38:5B:10:E2', "outside")
    sensor3 = LYWSD03MMC_reader('A4:C1:38:D2:7A:00', "filament")
    sensor4 = LYWSDCGQ_reader('58:2D:34:38:3C:E2', "bathroom")

    # Default values
    kitchen_temp  = 0
    kitchen_hum   = 0
    kitchen_bat   = 0
    bathroom_temp = 0
    bathroom_hum  = 0
    bathroom_bat  = 0
    outside_temp  = 0
    outside_hum   = 0
    outside_bat   = 0
    filament_temp = 0
    filament_hum  = 0
    filament_bat  = 0

    maxRetryCounter = 3

    retryCounter = 0
    while 1:
        ret = sensor1.read_data()
        if ret is not None:
            logger.log(f"Data from {sensor1.name} ({sensor1.mac}): {ret}")
            #sensor1JSON=f'{sensor1.name}-temperature={ret["temperature"]}&{sensor1.name}-humidity={ret["humidity"]}&{sensor1.name}-battery={ret["battery"]}'
            kitchen_temp = ret["temperature"]
            kitchen_hum  = ret["humidity"]
            kitchen_bat  = ret["battery"]
            break
        else:
            logger.log(f"Empty data from {sensor1.name} ({sensor1.mac}), retrying...", messageType = "WARN")
            retryCounter+=1
            if retryCounter > maxRetryCounter:
                #sensor1JSON=f'{sensor1.name}-temperature=0&{sensor1.name}-humidity=0&{sensor1.name}-battery=0'
                logger.log(f"Couldn't connect to the sensor {maxRetryCounter} times to {sensor1.name} ({sensor1.mac})!", messageType = "ERROR")
                break


    retryCounter = 0
    while 1:
        ret = sensor2.read_data()
        if ret is not None:
            logger.log(f"Data from {sensor2.name} ({sensor2.mac}): {ret}")
            #sensor2JSON=f'{sensor2.name}-temperature={ret["temperature"]}&{sensor2.name}-humidity={ret["humidity"]}&{sensor2.name}-battery={ret["battery"]}'
            outside_temp = ret["temperature"]
            outside_hum  = ret["humidity"]
            outside_bat  = ret["battery"]
            break
        else:
            logger.log(f"Empty data from {sensor2.name} ({sensor2.mac}), retrying...", messageType = "WARN")
            retryCounter+=1
            if retryCounter > maxRetryCounter:
                #sensor2JSON=f'{sensor2.name}-temperature=0&{sensor2.name}-humidity=0&{sensor2.name}-battery=0'
                logger.log(f"Couldn't connect to the sensor {maxRetryCounter} times to {sensor2.name} ({sensor2.mac})!", messageType = "ERROR")
                break

    retryCounter = 0
    while 1:
        ret = sensor3.read_data()
        if ret is not None:
            logger.log(f"Data from {sensor3.name} ({sensor3.mac}): {ret}")
            #sensor3JSON=f'{sensor3.name}-temperature={ret["temperature"]}&{sensor3.name}-humidity={ret["humidity"]}&{sensor3.name}-battery={ret["battery"]}'
            filament_temp = ret["temperature"]
            filament_hum  = ret["humidity"]
            filament_bat  = ret["battery"]
            break
        else:
            logger.log(f"Empty data from {sensor3.name} ({sensor3.mac}), retrying...", messageType = "WARN")
            retryCounter+=1
            if retryCounter > maxRetryCounter:
                #sensor3JSON=f'{sensor3.name}-temperature=0&{sensor3.name}-humidity=0&{sensor3.name}-battery=0'
                logger.log(f"Couldn't connect to the sensor {maxRetryCounter} times to {sensor3.name} ({sensor3.mac})!", messageType = "ERROR")
                break

    retryCounter = 0
    while 1:
        ret = sensor4.read_data()
        if ret is not None:
            logger.log(f"Data from {sensor4.name} ({sensor4.mac}): {ret}")
            #sensor4JSON=f'{sensor4.name}-temperature={ret["temperature"]}&{sensor4.name}-humidity={ret["humidity"]}&{sensor4.name}-battery={ret["battery"]}'
            bathroom_temp = ret["temperature"]
            bathroom_hum  = ret["humidity"]
            bathroom_bat  = ret["battery"]
            break
        else:
            logger.log(f"Empty data from {sensor4.name} ({sensor4.mac}), retrying...", messageType = "WARN")
            retryCounter+=1
            if retryCounter > maxRetryCounter:
                #sensor4JSON=f'{sensor4.name}-temperature=0&{sensor4.name}-humidity=0&{sensor4.name}-battery=0'
                logger.log(f"Couldn't connect to the sensor {maxRetryCounter} times to {sensor4.name} ({sensor4.mac})!", messageType = "ERROR")
                break

    #upload_data = f"{sensor1JSON}&{sensor2JSON}&{sensor3JSON}&{sensor4JSON}"

    # Connect to Firebase Firestore
    cred = credentials.Certificate("home-sensors-credentials.json")
    firebase_admin.initialize_app(cred)

    firestore_db = firestore.client()
    collection = firestore_db.collection('home_sensors_v1')

    #example timestamp: "20201204-122331"
    timestampFormat ='%Y%m%d-%H%M%S'

    collection.add({'date': datetime.now(), 'timestamp': datetime.now().strftime(timestampFormat), 
                    'kitchen_temp': kitchen_temp, 'kitchen_hum': kitchen_hum, 'kitchen_bat': kitchen_bat,
                    'bathroom_temp': bathroom_temp, 'bathroom_hum': bathroom_hum, 'bathroom_bat': bathroom_bat,
                    'outside_temp': outside_temp, 'outside_hum': outside_hum, 'outside_bat': outside_bat,
                    'filament_temp': filament_temp, 'filament_hum': filament_hum, 'filament_bat': filament_bat
    })

    # Gracefully stop watchdog
    shutdownFlag.set()
    watchdogThread.join()