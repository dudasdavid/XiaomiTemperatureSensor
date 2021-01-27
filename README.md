# XiaomiTemperatureSensor

# Dependencies:
sudo apt install bluetooth libbluetooth-dev  
sudo apt-get install libglib2.0-dev  
sudo apt install python3-pip  
pip3 install pybluez  
pip3 install bluepy  


sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)

# Fix Ubuntu 20.04 hcitool issue:
sudo ln -s /lib/firmware /etc/firmware  
sudo hciattach /dev/ttyAMA0 bcm43xx 921600 -  
```console
ubuntu@ubuntu:~/git/XiaomiTemperatureSensor$ sudo ln -s /lib/firmware /etc/firmware
ubuntu@ubuntu:~/git/XiaomiTemperatureSensor$ sudo hcitool dev
Devices:
ubuntu@ubuntu:~/git/XiaomiTemperatureSensor$ sudo hciattach /dev/ttyAMA0 bcm43xx 921600 -
bcm43xx_init
Set Controller UART speed to 921600 bit/s
Flash firmware /etc/firmware/brcm/BCM4345C0.hcd
Set Controller UART speed to 921600 bit/s
Device setup complete
ubuntu@ubuntu:~/git/XiaomiTemperatureSensor$ sudo hcitool dev
Devices:
        hci0    43:45:C0:00:1F:AC
```

# Get MAC address:
sudo hcitool lescan --duplicate  

