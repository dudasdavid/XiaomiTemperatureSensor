# XiaomiTemperatureSensor

## Dependencies:
First install the following dependencies:
```bash
sudo apt install bluetooth libbluetooth-dev  
sudo apt-get install libglib2.0-dev  
sudo apt install python3-pip  
pip3 install pybluez  
pip3 install btlewrap
pip3 install bluepy  
```

Bluetooth LE Scanning needs root privileges, to run the script as normal user, execute:  
```bash
sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f `which python3`)
```

## Fix Ubuntu 20.04 hcitool issue:
Out of the box, the BLE interface doesn't work on Raspberry Pi with Ubuntu 20.04 server. (2021.01.28)  
To fix this issue execute:
```bash
sudo ln -s /lib/firmware /etc/firmware  
sudo hciattach /dev/ttyAMA0 bcm43xx 921600 -  
```
Output should look like this:
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

## Get MAC address of the sensors:
```bash
sudo hcitool lescan --duplicate  
```
or
```bash
sudo hcitool lescan  
```

### My MAC addresses:  
`'58:2D:34:38:3C:E2'` - LYWSDCGQ  
`'A4:C1:38:EA:1D:CC'` - LYWSD03MMC kitchen  
`'A4:C1:38:5B:10:E2'` - LYWSD03MMC outside  
`'A4:C1:38:D2:7A:00'` - LYWSD03MMC filament  

## Current status:
It can read data from LYWSDCGQ, has to be upgraded to use with LYWSD03MMC, too!  

## Sources:  
https://github.com/JsBergbau/MiTemperature2  
https://github.com/ratcashdev/mitemp  
https://github.com/erdose/xiaomi-mi-lywsd03mmc
