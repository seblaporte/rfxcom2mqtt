import os
from dotenv import load_dotenv

load_dotenv()

LOGLEVEL = os.getenv("LOGLEVEL")
MQTT_PREFIX = os.getenv("MQTT_PREFIX")
MQTT_HOMEASSISTANT = os.getenv("MQTT_HOMEASSISTANT")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
RFX_PORT = os.getenv("RFX_PORT")
RFX_DEBUG = os.getenv("RFX_DEBUG")
RFX_DEVICE_PREFIX = os.getenv("RFX_DEVICE_PREFIX")
if RFX_DEBUG == "False":
    RFX_DEBUG = False

KNOWNDEVICES = {}
KNOWNDEVICESTYPE = {}
knowndevices_name = "knowndevices.ini"
if os.path.isfile(knowndevices_name):
    with open(knowndevices_name) as convertfile:
        lines = convertfile.read().splitlines()
        for line in lines:
            parts = line.split("=")
            KNOWNDEVICES[parts[0]] = parts[1]           
            KNOWNDEVICESTYPE[parts[1]] = parts[2]

UNKNOWNDEVICES = {}
unknowndevices_name = "unknowndevices.ini"            
def majunknown():
    if os.path.isfile(unknowndevices_name):
        with open(unknowndevices_name) as convertfile:
            lines = convertfile.read().splitlines()
            for line in lines:
                parts = line.split("=")
                UNKNOWNDEVICES[parts[0]] = parts[1]
majunknown()                