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
