# python 3.6

import random
import json
import time
from datetime import datetime
from random import randrange, uniform

from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "slt/uwe"
machineid = 126547
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):

    while True:
        time.sleep(1)
        randNumber = round(uniform(0, 100),2)
        now = datetime.now()
        day = now.strftime("%d-%m-%Y")
        clock = now.strftime("%H:%M:%S")
        data = {
            'Factor':'Temperature',
            'MachineID':machineid, 
            'Level':randNumber,
            'Date':day,
            'Time': clock
            }
        if (randNumber>=80):
            data['Status']='Critical'
        elif (80 > randNumber >= 55):
            data['Status']='Warning'
        else:
            data['Status']='Info'
        j_msg = json.dumps(data)
        msg = j_msg
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
