import json
import time
import logging
import paho.mqtt.client as mqtt
from RFXtrx import PySerialTransport, SensorEvent, ControlEvent, StatusEvent, get_device
from settings import *

loglevel = logging.getLevelName(LOGLEVEL)
logging.basicConfig(level=loglevel, filename="RFXlog.log")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("MQTT Connected with result code " + str(rc) + ": " + mqtt.connack_string(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PREFIX + "/switch/#")
    connect_topic = MQTT_PREFIX + "/status"
    mqtt_client.publish(connect_topic,payload="connected", qos=0, retain=True)
  

def on_disconnect():
    mqtt_client.publish(connect_topic,payload="disconnected", qos=0, retain=True)       
                
def id_to_name(id_string):
    if id_string in KNOWNDEVICES.keys():
        return KNOWNDEVICES[id_string]
    return id_string

def id_to_mqttname(id_string):
    if id_string in KNOWNDEVICES.keys():    
        devicename = id_to_name(id_string)
        return name_to_mqttname(devicename)
    return id_string

def name_to_mqttname(name_string):    
    name_string = RFX_DEVICE_PREFIX+"_" + name_string
    return name_string
    
def mqttname_to_id(topic):
    devicename=topic.replace(MQTT_PREFIX + "/switch/" + RFX_DEVICE_PREFIX + "_","")
    devicename=devicename.replace("/set","")
    if devicename in KNOWNDEVICES.values():
        idkey=[c for c,v in KNOWNDEVICES.items() if v==devicename]
        return idkey[0]
    return "not found !"
    
def isknown(id_string):
    if id_string in KNOWNDEVICES.keys():
        return True
    else:
        return False

def isunknown(id_string):
    if id_string in UNKNOWNDEVICES.keys():
        return True
    else:
        return False
        
def as_temperature(devicetype):
    if (devicetype.find('T') != -1):
        return True
    else:
        return False
def as_humidity(devicetype):
    if (devicetype.find('H') != -1):
        return True
    else:
        return False
        
def as_battery(devicetype):
    if (devicetype.find('B') != -1):
        return True
    else:
        return False 
def is_chacon(devicetype):
    if (devicetype.find('AC') != -1):
        return True
    else:
        return False         
def is_motion(devicetype):
    if (devicetype.find('S') != -1):
        return True
    else:
        return False         
        
def del_haconfig():
    for devicename,devicetype in KNOWNDEVICESTYPE.items():
        devicename=name_to_mqttname(devicename)
        if (devicename != "RFXCOM_ID"):
            logging.debug("Known device: " + str(devicename) +  " -> type: " + str(devicetype))
            if as_temperature(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_T/config"
                json_payload = '{}'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=False)
            if as_humidity(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_H/config"
                json_payload = '{}'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=False)
            if as_battery(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_B/config"
                json_payload = '{}'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=False)
                
def init_haconfig():
    for devicename,devicetype in KNOWNDEVICESTYPE.items():
        devicename=name_to_mqttname(devicename)
        if (devicename != "RFXCOM_ID"):
            #GATEWAY STATE SENSOR
            mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/"+ MQTT_PREFIX + "_gateway/config"
            json_payload = '{ "device_class": "connectivity", "name": "' + MQTT_PREFIX + '_gateway", "state_topic": "' + MQTT_PREFIX + '/status", "value_template":"{{ \'ON\' if \'connected\' in value else \'OFF\'}}","device":{"manufacturer":"Yvon_Indel","name":"RfxcomMqtt Gateway","model":"rfxcom2mqtt_gateway","sw_version":"1.0","identifiers":"rfxcom2mqtt-001"}}'
            logging.debug(mqtt_topic + ": " + json_payload)
            mqtt_client.publish(mqtt_topic, json_payload,retain=True)
            #SENSORS
            logging.debug("Known device: " + str(devicename) +  " -> type: " + str(devicetype))
            if as_temperature(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_T/config"
                json_payload = '{ "device_class": "temperature", "name": "' + devicename + '_T", "state_topic": "' + MQTT_PREFIX + '/sensor/' + devicename + '/state", "unit_of_measurement": "°C","value_template": "{{ value_json.Temperature }}","availability_topic":"' + MQTT_PREFIX + '/status","payload_available":"connected","payload_not_available":"disconnected" }'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=True)
            if as_humidity(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_H/config"
                json_payload = '{ "device_class": "humidity", "name": "' + devicename + '_H", "state_topic": "' + MQTT_PREFIX + '/sensor/' + devicename + '/state", "unit_of_measurement": "%","value_template": "{{ value_json.Humidity }}","availability_topic":"' + MQTT_PREFIX + '/status","payload_available":"connected","payload_not_available":"disconnected" }'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=True)
            if as_battery(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/sensor/" + devicename + "_B/config"
                json_payload = '{ "device_class": "battery", "name": "' + devicename + '_B", "state_topic": "' + MQTT_PREFIX + '/sensor/' + devicename + '/state","value_template": "{{ value_json.Battery_numeric }}","availability_topic":"' + MQTT_PREFIX + '/status","payload_available":"connected","payload_not_available":"disconnected" }'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=True)
            #SWITCH OR REMOTE
            if is_chacon(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/switch/" + devicename + "/config"
                json_payload = '{"name": "' + devicename +'", "state_topic": "' + MQTT_PREFIX + '/switch/' + devicename + '/state", "command_topic": "' + MQTT_PREFIX + '/switch/' + devicename + '/set","availability_topic":"' + MQTT_PREFIX + '/status","payload_available":"connected","payload_not_available":"disconnected" }'
                logging.debug(mqtt_topic + ": " + json_payload)
                mqtt_client.publish(mqtt_topic, json_payload,retain=True)
            #MOTION SENSOR
            if is_motion(devicetype):
                mqtt_topic = MQTT_HOMEASSISTANT + "/binary_sensor/" + devicename + "/config"
                json_payload = '{ "device_class": "motion", "name": "' + devicename+'", "state_topic": "' + MQTT_PREFIX + '/binary_sensor/' + devicename + '/state","availability_topic":"' + MQTT_PREFIX + '/status","payload_available":"connected","payload_not_available":"disconnected" }'
                mqtt_client.publish(mqtt_topic, json_payload,retain=True)

def switch_turn_on(deviceid):
    #transport.reset()
    x = get_device(0x11, 0x00, deviceid)
    x.send_on(transport)
    state_topic = MQTT_PREFIX + '/switch/' + id_to_mqttname(deviceid) + '/state'
    mqtt_client.publish(state_topic,payload="ON", qos=0, retain=True)
    logging.debug("Device " + deviceid + " is turned ON")
    print("Device " + deviceid + " is turned ON")


def switch_turn_off(deviceid):
    #transport.reset()
    x = get_device(0x11, 0x00, deviceid)
    x.send_off(transport)
    state_topic = MQTT_PREFIX + '/switch/' + id_to_mqttname(deviceid) + '/state'
    mqtt_client.publish(state_topic,payload="OFF", qos=0, retain=True)
    logging.debug("Device " + deviceid + " is turned OFF")
    print("Device " + deviceid + " is turned OFF")

def sensor_turn_on(deviceid):
    state_topic = MQTT_PREFIX + '/binary_sensor/' + id_to_mqttname(deviceid) + '/state'
    mqtt_client.publish(state_topic,payload="ON", qos=0, retain=True)
    logging.debug("Device " + deviceid + " is turned ON")
    print("Device " + deviceid + " is turned ON")


def sensor_turn_off(deviceid):
    state_topic = MQTT_PREFIX + '/binary_sensor/' + id_to_mqttname(deviceid) + '/state'
    mqtt_client.publish(state_topic,payload="OFF", qos=0, retain=True)
    logging.debug("Device " + deviceid + " is turned OFF")
    print("Device " + deviceid + " is turned OFF")

    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic= msg.topic
    message= msg.payload.decode('utf-8')
    deviceid=mqttname_to_id(topic)
    if deviceid == "not found!":
        logging.debug("topic received: " + topic + " device name not found in knowndevices.ini !")
        print("topic received: " + topic + " device name not found in knowndevices.ini !")
    else:
        if KNOWNDEVICESTYPE[id_to_name(deviceid)] == "AC":
            if message == "ON":
                switch_turn_on(deviceid)
            else:               
                if message == "OFF":
                    switch_turn_off(deviceid)
                else:
                    logging.debug("Device command received for " + deviceid + " is not currently handled (" + message + ")")
                    print("Device command received for " + deviceid + " is not currently handled (" + message + ")")
        else:
            logging.debug("Device type of : " + deviceid + " is not currently handled (" + KNOWNDEVICESTYPE[deviceid] + ")")
            print("Device type of : " + deviceid + " is not currently handled (" + KNOWNDEVICESTYPE[deviceid] + ")")
 
transport = PySerialTransport(RFX_PORT, debug=RFX_DEBUG)
mqtt_client = mqtt.Client()  # Create the client
mqtt_client.on_connect = on_connect  # Callback on when connected
mqtt_client.on_message = on_message  # Callback when message received
mqtt_client.on_disconnect = on_disconnect # Callback when disconnected
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)  # Set user and pw
mqtt_client.will_set(MQTT_PREFIX + "/status", payload="disconnected", qos=0, retain=True) # Set last will and testament when disconnected
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)  # Connect the MQTT Client

mqtt_client.loop_start()


#del_haconfig
init_haconfig()

     
infinitloop=True

while infinitloop:
    event = transport.receive_blocking()

    if event is None:
        continue

    logging.debug(event)
    if isunknown(event.device.id_string):
        logging.debug("Device not configured: " + event.device.id_string)
        print("Device not configured: " + event.device.id_string) 
    else:
        if not isknown(event.device.id_string):
            logging.debug("New device detected : " + event.device.id_string)
            f = open("unknowndevices.ini", "a")
            f.write("\r\n" + event.device.id_string+"="+str(vars(event.device)))
            f.close()
            logging.debug("New device added to unknowndevices.ini ")
            print("New device added to unknowndevices.ini ")
            majunknown()
                
    if isinstance(event, SensorEvent):
        if isknown(event.device.id_string):
            devicename = id_to_name(event.device.id_string)
            devicename=RFX_DEVICE_PREFIX+"_" + devicename
            logging.debug("Known device: " + devicename)
            parsed_json = event.values
            print(parsed_json)
            clean_json = {}
            for key, value in parsed_json.items():
                cleankey=key.replace(" ","_")
                clean_json[cleankey] = value
            mqtt_topic = MQTT_PREFIX + "/sensor/" + devicename + "/state"
            json_payload = json.dumps(clean_json)
            logging.debug(mqtt_topic + ": " + json_payload)
            mqtt_client.publish(mqtt_topic, json_payload)

    if isinstance(event, ControlEvent):
        # mqtt_topic = MQTT_PREFIX + "/control/" + id_to_name(event.device.id_string)
        # json_payload = json.dumps(event.values)
        # logging.info(mqtt_topic + ": " + json_payload)
        # mqtt_client.publish(mqtt_topic, json_payload)
        if isknown(event.device.id_string):
            deviceid=event.device.id_string
            if KNOWNDEVICESTYPE[id_to_name(deviceid)] == "AC":
                print(event.values)
                message=event.values["Command"].upper()
                print(message)
                if message == "ON":
                    switch_turn_on(deviceid)
                else:               
                    if message == "OFF":
                        switch_turn_off(deviceid)
                    else:
                        logging.debug("Device command received for " + str(deviceid) + " is not currently handled (" + message + ")")
                        print("Device command received for " + srt(deviceid) + " is not currently handled (" + message + ")")
            
            if KNOWNDEVICESTYPE[id_to_name(deviceid)] == "S":
                print(event.values)
                message=event.values["Command"].upper()
                print(message)
                if message == "ON":
                    sensor_turn_on(deviceid)
                else:               
                    if message == "OFF":
                        sensor_turn_off(deviceid)
                    else:
                        logging.debug("Device command received for " + str(deviceid) + " is not currently handled (" + message + ")")
                        print("Device command received for " + srt(deviceid) + " is not currently handled (" + message + ")")
            else:
                logging.debug("Device type of : " + str(deviceid) + " is not currently handled (" + KNOWNDEVICESTYPE[deviceid] + ")")
                print("Device type of : " + str(deviceid) + " is not currently handled (" + KNOWNDEVICESTYPE[deviceid] + ")")

    if isinstance(event, StatusEvent):
        # mqtt_topic = MQTT_PREFIX + "/status"
        # logging.error("Statusevent: " + str(event))
        # mqtt_client.publish(mqtt_topic, "StatusEvent received, cannot handle: " + str(event))
        print("*********************** Statut *****************************")
        print(event)
        print(event.device.id_string)
        print(id_to_name(event.device.id_string))

mqtt_client.disconnect()