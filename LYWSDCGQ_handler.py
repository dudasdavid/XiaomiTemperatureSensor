#!/usr/bin/env python3
from bluepy.btle import DefaultDelegate
from datetime import datetime

timestampFormat ='%Y-%m-%d,%H:%M:%S:%f'

class LYWSDCGQ_delegate(DefaultDelegate):
    def __init__(self, q):
        DefaultDelegate.__init__(self)
        self.queue = q

    def handleNotification(self, cHandle, data):  # pylint: disable=unused-argument,invalid-name
        if data is None:
            print("Some debug message")
            return
        data = data.decode("utf-8").strip(' \n\t')
        data = data.strip('\0')
        data = ''.join(filter(lambda i: i.isprintable(), data))

        res = dict()
        for dataitem in data.split(' '):
            dataparts = dataitem.split('=')
            if dataparts[0] == 'T':
                res["temp"] = float(dataparts[1])
            elif dataparts[0] == 'H':
                res["hum"] = float(dataparts[1])

        timeStamp = datetime.now().strftime(timestampFormat)
        self.queue.put([timeStamp, res])

    def get_comfort_type(self, humidity):
        comfort_type = '0'
        if float(humidity) < 40:
            comfort_type = '2'
        elif float(humidity) <= 70:
            comfort_type = '1'
        elif float(humidity) > 70:
            comfort_type = '3'
        return comfort_type



