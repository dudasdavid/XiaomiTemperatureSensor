#!/usr/bin/env python3
from bluepy.btle import DefaultDelegate, Peripheral
import bluepy

from SimpleLogger import SimpleLogger

from datetime import datetime
import queue

timestampFormat ='%d/%m/%Y-%H:%M:%S'

class LYWSDCGQ_reader:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.logger = SimpleLogger(verbose = True, loggerName = f"Sensor-{name}-{mac}")

        self.retryCounter = 0
        self.maxRetryCounter = 4

        self.p = None
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

        if self.p == None:
            return None

        try:
            self.p.connect(self.mac)
            #firmware = self.p.readCharacteristic(0x0024)
            battery = self.p.readCharacteristic(0x0018)
            battery = int(ord(battery))

            self.p.writeCharacteristic(0x0010, b'\x01\x00', True)      #enable notifications of Temperature and Humidity
            self.p.withDelegate(LYWSDCGQ_delegate(self.q))
            self.wait_for_notification()
            self.p.disconnect()
            self.logger.log(f"Reading was successful on {self.name} ({self.mac})!", messageType = "OK")

            temp = self.q.get()
            temp["battery"]=battery
            self.q.put(temp)

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


class LYWSDCGQ_delegate(DefaultDelegate):
    def __init__(self, q):
        DefaultDelegate.__init__(self)
        self.queue = q

    def handleNotification(self, cHandle, data):
        if data is None:
            self.logger.log(f"Empty data from {self.name} ({self.mac})", messageType = "WARN")
            return
        data = data.decode("utf-8").strip(' \n\t')
        data = data.strip('\0')
        data = ''.join(filter(lambda i: i.isprintable(), data))

        ret = dict()
        for dataitem in data.split(' '):
            dataparts = dataitem.split('=')
            if dataparts[0] == 'T':
                ret["temperature"] = float(dataparts[1])
            elif dataparts[0] == 'H':
                ret["humidity"] = float(dataparts[1])

        timeStamp = datetime.now().strftime(timestampFormat)
        ret["time"] = timeStamp

        self.queue.put(ret)




