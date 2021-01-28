#!/usr/bin/env python3

from LYWSD03MMC_handler import LYWSD03MMC_delegate
from LYWSDCGQ_handler import LYWSDCGQ_delegate

from bluepy.btle import Peripheral
import bluepy
import time
import queue
from SimpleLogger import SimpleLogger

class LYWSD03MMC_reader:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.logger = SimpleLogger(verbose = True, loggerName = f"Sensor-{name}-{mac}")

        while 1:
            try:
                self.p = Peripheral(self.mac)
                self.p.disconnect()
                break
            except bluepy.btle.BTLEDisconnectError as e:
                self.logger.log(f"BLE disconnect error: {e}", messageType = "ERROR", forcePrint = True)

        self.q = queue.Queue()
        

    def handle_temp_hum_value(self):
        while True:
            if self.p.waitForNotifications(10.0):
                break

    def read_data(self):
        self.logger.log(f"Start reading data from {self.name} ({self.mac})", messageType = "DEBUG")
        try:
            self.p.connect(self.mac)
            self.p.writeCharacteristic(0x0038, b'\x01\x00', True)      #enable notifications of Temperature, Humidity and Battery voltage
            self.p.writeCharacteristic(0x0046, b'\xf4\x01\x00', True)
            self.p.withDelegate(LYWSD03MMC_delegate(self.q))
            self.handle_temp_hum_value()
            self.p.disconnect()
            self.logger.log(f"Reading was successful on {self.name} ({self.mac})!", messageType = "OK")
        except bluepy.btle.BTLEDisconnectError as e:
            self.logger.log(f"BLE disconnect error: {e} on {self.name} ({self.mac})", messageType = "ERROR", forcePrint = True)

        self.process_queue()

    def process_queue(self):
        qsize = self.q.qsize()
        self.logger.log(f"Queue size on {self.name} ({self.mac}): {qsize}", messageType = "DEBUG")
        if qsize > 0:
            data = self.q.get()
            self.logger.log(f"Data from {self.name} ({self.mac}): {data}")
            

class LYWSDCGQ_reader:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.logger = SimpleLogger(verbose = True, loggerName = f"Sensor-{name}-{mac}")

        while 1:
            try:
                self.p = Peripheral(self.mac)
                self.p.disconnect()
                break
            except bluepy.btle.BTLEDisconnectError as e:
                self.logger.log(f"BLE disconnect error: {e}", messageType = "ERROR", forcePrint = True)

        self.q = queue.Queue()
        

    def handle_temp_hum_value(self):
        while True:
            if self.p.waitForNotifications(10.0):
                break

    def read_data(self):
        self.logger.log(f"Start reading data from: {self.mac}")
        try:
            self.p.connect(self.mac)
            self.p.writeCharacteristic(0x0010, b'\x01\x00', True)      #enable notifications of Temperature, Humidity and Battery voltage
            self.p.withDelegate(LYWSDCGQ_delegate(self.q))
            self.handle_temp_hum_value()
            self.p.disconnect()
            self.logger.log(f"Reading was successful!", messageType = "OK")
        except bluepy.btle.BTLEDisconnectError as e:
            self.logger.log(f"BLE disconnect error: {e}", messageType = "ERROR", forcePrint = True)

        self.process_queue()

    def process_queue(self):
        qsize = self.q.qsize()
        self.logger.log(f"Queue size: {qsize}")
        if qsize > 0:
            data = self.q.get()
            self.logger.log(f"Data from {self.mac}: {data}")

'''
MAC Addresses:
'58:2D:34:38:3C:E2' - LYWSDCGQ  
'A4:C1:38:EA:1D:CC' - LYWSD03MMC kitchen  
'A4:C1:38:5B:10:E2' - LYWSD03MMC outside  
'A4:C1:38:D2:7A:00' - LYWSD03MMC filament  
'''
        

#sensor1 = LYWSD03MMC_reader('A4:C1:38:EA:1D:CC', "kitchen")
#sensor2 = LYWSD03MMC_reader('A4:C1:38:5B:10:E2', "outside")
#sensor3 = LYWSD03MMC_reader('A4:C1:38:D2:7A:00', "filament")
sensor4 = LYWSDCGQ_reader('58:2D:34:38:3C:E2', "bathroom")

for i in range(10):
    #sensor1.read_data()
    #time.sleep(10)
    #sensor2.read_data()
    #time.sleep(10)
    #sensor3.read_data()
    #time.sleep(10)
    sensor4.read_data()
    time.sleep(10)

