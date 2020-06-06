# rfxcom-mqtt-gateway

A  Python script which provides a Rfxcom to MQTT gateway for my own use with [Home Assistant](https://www.home-assistant.io/docs/)

I use an old rfxtr433 model which doesn't support the Somfy protocol.

## Features

* Data publication via MQTT
* Auto discovery in Home Assistant
* MQTT authentication support
* Systemd service
* I hope reliable
* Tested on Raspberry Pi 1

### Supported devices

* Oregon THR128
* Oregon THX122NR
* [Chacon sockets](https://chacon.com/en/remote-controlled-sockets/614-set-of-3-on-off-remote-controlled-sockets-and-3-channel-remote-control-5411478546603.html)
* Chacon remote control (black one)
* [Motion Sensor X10 MS16A](https://www.x10.com/ms16a.html)
* I guess all devices with AC protocol should be supported.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* `python3` >= 3.5
* `pip3`
* `git`

## Installation

### Virtualenv
On a modern Linux system, just a few steps are needed to get the gateway working.
The following example shows the installation under Raspbian:

```shell
sudo apt-get install git python3 python3-pip
sudo pip3 install virtualenv
git clone https://github.com/Yvon-Indel/rfxcom-mqtt-gateway.git
cd rfxcom-mqtt-gateway
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Configuration

Create the file .env and change the information according to your own need:
```sh
MQTT_PREFIX = rfxcom
MQTT_HOMEASSISTANT = homeassistant
MQTT_HOST = 192.168.1.27
MQTT_PORT = 1883
MQTT_USER = login
MQTT_PASS = password
RFX_PORT = /dev/ttyUSB0
RFX_DEBUG = True
RFX_DEVICE_PREFIX = rfxcom
```
#### Detect new device
When a new device is detected by the rfxcom, an entry is created in the file "unknowndevices.ini".
You can find the id of all detected device inside this file.

Exemple:
```sh
1e0eb92:2={'packettype': 17, 'subtype': 0, 'type_string': 'AC', 'id_string': '1e0eb92:2', 'known_to_be_dimmable': False, 'known_to_be_rollershutter': False, 'id_combined': 31517586, 'unitcode': 2}={'packettype': 17, 'subtype': 0, 'type_string': 'AC', 'id_string': '1e0eb92:2', 'known_to_be_dimmable': False, 'known_to_be_rollershutter': False, 'id_combined': 31517586, 'unitcode': 2}
```
The device id is 1e0eb92:2
#### Add a device to HA
To use a device in HA, you have to add an entry in "knowndevices.ini"
> ***Attention : don't remove the first line of the file "RFXCOM_ID=human_readable_name=type"
##### OREGON device:
Exemple:
```sh
fc:04=salle_de_bain_bas=THB
```
  - fc:04 is device id
  - salle_de_bain_bas is the name of the sensor in HA
  - T means the device as temperature payload
  - H means the device as humidity payload
  - B means the device as battery payload
  
If the device as only temperature and battery payload, you can add:
```sh
fc:04=salle_de_bain_bas=TB
```
If you only need temperature, you can add:
```sh
fc:04=salle_de_bain_bas=T
```
##### AC device (like Chacon remote control)

Add an entry like this:
```sh
1e0eb92:1=Remote_1_Bt1=AC
```
  - 1e0eb92:1 is the device id
  - Remote_1_Bt1 is the name of the sensor in HA
  - AC means it's an AC device.

##### X10 Motion Sensor

Add an entry like this:
```sh
A13=detecteur_chevet=S
```
  - A13 is the device id
  - detecteur_chevet is the name of the sensor in HA
  - S means it's an X10 motion sensor device.

## Execution

A test run is as easy as:

```shell
source .venv/bin/activate
sudo ./rfxcom_gateway.py
```

## Deployment

Continuous background execution can be done using the example Systemd service unit provided.
   
```shell
Edit and modify path of rfxcom-mqtt-gateway in the rfxcom-mqtt-gateway.service file to match you own need
sudo cp rfxcom-mqtt-gateway.service /etc/systemd/system/
sudo systemctl enable rfxcom-mqtt-gateway.service
```
To start the service do :
```shell
sudo service rfxcom-mqtt-gateway start 
```
To watch the service status :
```shell
sudo service rfxcom-mqtt-gateway status
```
To stop the service :
```shell
sudo service rfxcom-mqtt-gateway stop
```

**Attention:**
You need to define the absolute path of `service.sh` in `rfxcom-mqtt-gateway.service`.

**Testing mqtt:**
Use [MqttBox](http://workswithweb.com/mqttbox.html) to print all messages.

## To do
There is no error handling, so the gateway could crash, please report issues.

## Authors

It's my own (dirty, i know) code, based on the work of thes github repo:

* Danielhiversen at https://github.com/Danielhiversen/pyRFXtrx 

* IcyPalm at https://github.com/IcyPalm/RFXCOM-MQTT-bridge



## License

[GPL3-0](https://github.com/Yvon-Indel/rfxcom-mqtt-gateway/blob/master/LICENCE)
