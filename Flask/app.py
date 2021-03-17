from flask import Flask, jsonify, request, render_template, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from datetime import datetime 
import datetime

app = Flask(__name__)
app.debug = True #to set in staging development
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://is614team9:password@localhost:5432/is614team9db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Location, Sensor, Tables, Table_occupancy_data, Env_sensor_data, Occupancy_sensor_data

@app.route('/is614team9/getSensorReadings', methods = ['GET'])
def get_sensor_readings():
  return "Hello World"



