since nobody answered my query, about 
```
a Wemos D1 mini running tasmota that has 'DeepSleepTime 120' set.  In homeassistant, the temperature shows "Unavailable" when sleeping.   How to make Homeassistant keep the last value displayed?
```

I came up with a python script to change the LWT of DS1820 sensors running tasmota.   This python script keeps such sensors "live" on Homeassistant and lets the temp value continue to be displayed while the tasmota temperature sensor deep sleeps.

```
import paho.mqtt.client as mqtt
import daemon
import logging
import os

# MQTT broker details
BROKER = "your_mqtt_broker_address"
PORT = 1883
USERNAME = "your_username"
PASSWORD = "your_password"
TOPIC_SUB = "tele/tasmota_639206/LWT"  # change to suit your device
TOPIC_PUB = "tele/tasmota_639206/LWT"  # change to suit your device

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC_SUB)
    else:
        logging.error(f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if payload == "Offline":
        client.publish(TOPIC_PUB, "Online")

def run():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

with daemon.DaemonContext(
    stdout=open(os.devnull, 'w'),
    stderr=open(os.devnull, 'w')
):
    run()
```
