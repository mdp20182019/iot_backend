import base64
import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import ssl

client_mongo =MongoClient("mongodb+srv://Student:MDPESIB2018-2019@iot-cluster-saur7.mongodb.net/test?retryWrites=true"
                             ,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
db = client_mongo.test

# MQTT Settings
MQTT_Broker = "212.98.137.194"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic = "application/14/device/54d76ad0a462154c/rx"

#Subscribe to all Sensors at Base Topic
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_Topic)

#Save Data into DB Table
def on_message(client, userdata, msg):
    m = json.loads(msg.payload)
    print(m)
    received_data = base64.b64decode(m['data'])
    received_data
    print(received_data.decode('utf-8'))
    posts = db.RedH
    post_id = posts.insert_one(m).inserted_id
    print("Success")

client = mqtt.Client()
client.username_pw_set('user','bonjour')

# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
# Connect
client.connect(MQTT_Broker, MQTT_Port, Keep_Alive_Interval)
# Continue the network loop
client.loop_forever()