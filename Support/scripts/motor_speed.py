# python 3.6

import random
import json
import time
import itertools
from datetime import datetime
from random import randrange, uniform

import random
from paho.mqtt import client as mqtt_client

# initializing list
test_list = [11, 0, 55, 24, 73, 14, 42, 59, 21, 78]

broker = 'test.mosquitto.org'
port = 1883
topic = "slt/uwe"
machineid = 12644
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
        now = datetime.now()
        day = now.strftime("%d-%m-%Y")
        clock = now.strftime("%H:%M:%S")
        for i in itertools.count(start=1):
            rand_idx = random.randint(0, len(test_list)-1)
            random_num = test_list[rand_idx]

            if (random_num==0):
                print(f"captured {random_num}")
                time.sleep(5)
                data = {
                        'Factor':'MotorSpeed',
                        'MachineID':machineid, 
                        'Level':random_num,
                        'Date':day,
                        'Time': clock, 
                        'Status': 'Critical'
            }
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
