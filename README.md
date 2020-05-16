# rfxcom-mqtt-gateway

A  Python script which provides a Rfxcom to MQTT gateway for my own use.  

## Features

* Data publication via MQTT
* Auto discovery in Home Assistant
* MQTT authentication support
* Systemd service
* I hope reliable
* Tested on Raspberry Pi 1

### Supported devices

* [Oregon THR128]
* [Oregon THX122NR]
* [Chacon sockets](https://chacon.com/en/remote-controlled-sockets/614-set-of-3-on-off-remote-controlled-sockets-and-3-channel-remote-control-5411478546603.html)
* [Chacon remote control (black one)]
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

Work in progress

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
sudo service rfxcom-mqtt-gateway start
```
To stop the service :
```shell
sudo service rfxcom-mqtt-gateway stop
```

**Attention:**
You need to define the absolute path of `service.sh` in `rfxcom-mqtt-gateway.service`.

**Testing mqtt:**
Use mosquitto_sub to print all messages


## Authors




## License

