# python3.6

import random
import json
import mysql.connector
from paho.mqtt import client as mqtt_client

# Connection details for MYSQL Database
db = mysql.connector.connect(
    host='172.18.0.3',
    password='Austr@1ia', 
    user='root',
    database="sensor_data",
    port=3306
    )

# Check the connection to DB
if db.is_connected():
    print("connection established.....")
else:
    print("No")

# MQTT broker connection details
broker = 'test.mosquitto.org'
port = 1883
topic = "slt/uwe"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# Establish the connection with MQTT broker
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Subscribe the message from MQTT broker
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        #Decode and load JSON data
        y=json.loads(msg.payload.decode())
        LIST = (list(y.items()))
        print(LIST)
        dt = (y['Date'])
        clock = (y['Time'])
        mid = (y['MachineID'])
        fact = (y['Factor'])
        Lvl = (y['Level'])
        Stat = (y['Status'])
        val = dt, clock, mid, fact, Lvl, Stat
        
        # Insert the data into the MySQL database
        sqlcursor = db.cursor()
        col = "INSERT INTO data_table (Date, Time, MachineID, Factor, Level, Status) VALUES {}".format(val)
        print(col)
        sqlcursor.execute(col)
        db.commit()
        

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
