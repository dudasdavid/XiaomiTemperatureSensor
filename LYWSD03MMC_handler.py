#!/usr/bin/env python3
from bluepy.btle import DefaultDelegate, Peripheral
import bluepy

from SimpleLogger import SimpleLogger

from datetime import datetime
import queue

timestampFormat ='%d/%m/%Y-%H:%M:%S'

class LYWSD03MMC_reader:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.logger = SimpleLogger(verbose = True, loggerName = f"Sensor-{name}-{mac}")

        self.retryCounter = 0
        self.maxRetryCounter = 3
        while 1:
            try:
                self.p = Peripheral(self.mac)
                self.p.disconnect()
                self.logger.log(f"BLE connected to {self.name} ({self.mac})!", messageType = "OK")
                break
            except bluepy.btle.BTLEDisconnectError as e:
                self.logger.log(f"BLE disconnect error: {e} on {self.name} ({self.mac})", messageType = "ERROR")
                self.retryCounter += 1
                if self.retryCounter > self.maxRetryCounter:
                    self.logger.log(f"Couldn't connect {self.maxRetryCounter} times to {self.name} ({self.mac})", messageType = "ERROR")
                    break

        self.q = queue.Queue()
        

    def wait_for_notification(self):
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
            self.wait_for_notification()
            self.p.disconnect()
            self.logger.log(f"Reading was successful on {self.name} ({self.mac})!", messageType = "OK")
        except bluepy.btle.BTLEDisconnectError as e:
            self.logger.log(f"BLE disconnect error: {e} on {self.name} ({self.mac})", messageType = "ERROR")

        return self.process_queue()

    def process_queue(self):
        qsize = self.q.qsize()
        self.logger.log(f"Queue size on {self.name} ({self.mac}): {qsize}", messageType = "DEBUG")
        if qsize > 0:
            data = self.q.get()
            self.logger.log(f"Data from {self.name} ({self.mac}): {data}")
            return data
        else:
            return None

class LYWSD03MMC_delegate(DefaultDelegate):
    def __init__(self, q):
        DefaultDelegate.__init__(self)
        self.queue = q

    def handleNotification(self, cHandle, data):
        if data is None:
            self.logger.log(f"Empty data from {self.name} ({self.mac})", messageType = "WARN")
            return
        temperature = round(int.from_bytes(data[0:2],byteorder='little',signed=True)/100, 2)
        #print(f"Temperature: {temperature}")
        humidity = int.from_bytes(data[2:3],byteorder='little')
        #print(f"Humidity: {humidity}")
        voltage=int.from_bytes(data[3:5],byteorder='little') / 1000.
        #print(f"Voltage: {voltage}")
        batteryLevel = min(int(round((voltage - 2.1),2) * 100), 100)        #3.1 or above --> 100% 2.1 --> 0 %
        #print(f"Battery level: {batteryLevel}")

        timeStamp = datetime.now().strftime(timestampFormat)
        self.queue.put({"time":timeStamp, "temperature":temperature, "humidity":humidity, "voltage":voltage, "battery":batteryLevel})



