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

# telebot id: IS614_Team9_SystemHealth_Bot

my_token = '1675655344:AAFAs_r4UIWoSWQ5dx-iZxaoEQf-r3ik1io' # put your secret Telegram token here 
url_base = 'https://api.telegram.org/bot{}/'.format(my_token)

chat_id = '122673618'    # to change to group chat created

url_getUpdates = '{}getupdates'.format(url_base)
url_sendMsg = '{}sendMessage'.format(url_base)
url_editMessageText = '{}editMessageText'.format(url_base)


def send_telegram_alert(msg):
    global chat_id, url_sendMsg

    params = {'chat_id':chat_id, 'text':msg}
    r = requests.get(url=url_sendMsg, params = params)
    return

def system_health_check():
    # retrieves the last raw sensor record in the db every 15 minutes to check if the last seen is more than 15 minutes ago
    # if yes then an alert will be sent via a telegram bot!!
    while True:
        time_now = datetime.now()
        try:
            cur.execute('select "sensor_id", "sensor_type", max("timestamp") from env_sensor_data group by ("sensor_id", "sensor_type");')
            results = cur.fetchall()
            for r in results:
                time_difference = (time_now - r[2]).total_seconds() // 60
                if time_difference > 15:
                    msg = f"**Sensor System Health Alert**\nsensor id: {r[0]}\nsensor_type: {r[1]}\nLast seen: {r[2]}"
                    send_telegram_alert(msg)
        except Exception as e:
            print(e)
            
        time.sleep(900)
    return True

system_health_check()