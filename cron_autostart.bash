#!/usr/bin/env bash

sudo ln -s /lib/firmware /etc/firmware  
sudo hciattach /dev/ttyAMA0 bcm43xx 921600 -  

cd ~/git/XiaomiTemperatureSensor/
bash run.bash