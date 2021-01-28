#!/usr/bin/env python3
from bluepy.btle import DefaultDelegate
from datetime import datetime

timestampFormat ='%Y-%m-%d,%H:%M:%S:%f'

class LYWSD03MMC_delegate(DefaultDelegate):
    def __init__(self, q):
        DefaultDelegate.__init__(self)
        self.queue = q

    def handleNotification(self, cHandle, data):
        if data is None:
            print("Some debug message")
            return
        temperature = round(int.from_bytes(data[0:2],byteorder='little',signed=True)/100, 2)
        #print(f"Temp: {temperature}")
        humidity = int.from_bytes(data[2:3],byteorder='little')
        #print(f"Hum: {humidity}")
        voltage=int.from_bytes(data[3:5],byteorder='little') / 1000.
        #print(f"Voltage: {voltage}")
        batteryLevel = min(int(round((voltage - 2.1),2) * 100), 100)        #3.1 or above --> 100% 2.1 --> 0 %
        #print(f"Battery level: {batteryLevel}")
        comfort_type = self.get_comfort_type(humidity)
        #print(f"Comfort type: {comfort_type}")

        timeStamp = datetime.now().strftime(timestampFormat)
        self.queue.put([timeStamp, temperature, humidity, voltage, batteryLevel, comfort_type])

    def get_comfort_type(self, humidity):
        comfort_type = '0'
        if float(humidity) < 40:
            comfort_type = '2'
        elif float(humidity) <= 70:
            comfort_type = '1'
        elif float(humidity) > 70:
            comfort_type = '3'
        return comfort_type


