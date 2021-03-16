import paho.mqtt.client as mqttClient
import time
import json
import csv
import psycopg2
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import requests

conn = psycopg2.connect(host="127.0.0.1", dbname="is614team9db", user="is614team9", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
        
def insert_sensor_values_into_db(timestamp, sensor_ID, sensor_type, reading):
    if sensor_type == "noise" or sensor_type == "temp":
        try:
            cur.execute("""INSERT INTO env_sensor_data VALUES (DEFAULT, %s, %s, %s, %s)""", (timestamp, sensor_ID, sensor_type, reading))
            conn.commit()
            print("done") # for debugging
        except Exception as e:
            print(str(e))
    else:
        try:
            cur.execute("""INSERT INTO occupancy_sensor_data VALUES (DEFAULT, %s, %s, %s, %s)""", (timestamp, sensor_ID, sensor_type, reading))
            conn.commit()
            print("done") # for debugging
        except Exception as e:
            print(str(e))
    return


def on_message(client, userdata, message):
    data = message.payload.decode("utf-8").replace("'", '"')
    msg = json.loads(data)
    print(msg) # for debugging

    # to insert raw sensor values into db
    for i in range(len(msg['result'])):
        timestamp_unix = msg['timestamp']
        timestamp = datetime.utcfromtimestamp(timestamp_unix) + timedelta(hours=8)
        sensor_ID = msg['id']
        sensor_type = msg['result'][i]['type']
        reading = float(msg['result'][i]['reading'])

        print("trying to insert into db") # for debugging
        insert_sensor_values_into_db(timestamp, sensor_ID, sensor_type, reading)
        
    # TO DO: insert table occupancy data based on conditions
    
Connected = False   #global variable for the state of the connection
 
broker_address= "broker.mqttdashboard.com"  #Broker address
port = 1883                          #Broker port
user = "smt203team2"                    #Connection username
password = "smt203team2"            #Connection password
 
client = mqttClient.Client("yo")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
client.subscribe("chuchu/0987/tempnoise")
print("subscribed")
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print("exiting")    
    client.disconnect()
    client.loop_stop()
