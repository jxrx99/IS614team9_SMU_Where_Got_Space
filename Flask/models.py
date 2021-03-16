from app import db 
import datetime 

#creating table
class Location(db.Model):
    __tablename__ = 'location'

    location_id = db.Column(db.String(100), primary_key=True) 
    building = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), unique=False, nullable=False)
    area_name = db.Column(db.String(100), unique=False, nullable=False)

    #one-to-many model
    tables_L = db.relationship('Table', back_populates = 'locations', cascade ='all', lazy=True, uselist=True)

    def __init__(self, location_id, building, level, area_name): 
        self.location_id = location_id
        self.building = building
        self.level = level
        self.area_name = area_name

    def serialize(self): 
        return { 
            'location_id' : self.location_id ,
            'building' : self.building,
            'level' : self.level,
            'area_name' : self.area_name
        }

class Sensor(db.Model): 
    __tablename__ = 'sensor' #database table name, optionally specified 

    sensor_id = db.Column(db.String(100), primary_key=True)
    sensor_type = db.Column(db.String(30), primary_key=True) 
    sensor_deployment_date = db.Column(db.DateTime, nullable=False)
    table_id = db.Column(db.String(50), db.ForeignKey('tables.table_id'), unique=False, nullable=False)
    # to add in x and y once confirmed!!
    
    #one-to-many model
    tables_S = db.relationship('Tables', back_populates = 'sensors', cascade ='all', lazy=True, uselist=True)
    env_sensor_readings = db.relationship('Env_sensor_data', back_populates = 'sensor', cascade ='all', lazy=True, uselist=True)
    occupancy_sensor_readings = db.relationship('Occupancy_sensor_data', back_populates = 'sensor_1', cascade ='all', lazy=True, uselist=True)

    def __init__(self, sensor_id, sensor_type, sensor_deployment_date, location_id): 
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.sensor_deployment_date = sensor_deployment_date
        self.location_id = location_id

        #json format
    def serialize(self): 
        return { 
            'sensor_id' : self.sensor_id,
            'sensor_deployment_date' : self.sensor_deployment_date,
            'sensor_type' : self.sensor_type
        }

class Tables(db.Model): 
    __tablename__ = 'tables' #database table name, optionally specified 

    table_id = db.Column(db.String(100), primary_key=True)
    location_id = db.Column(db.String(50), db.ForeignKey('location.location_id'), unique=False, nullable=False)

    #one-to-many model   
    locations = db.relationship('Location', back_populates = 'tables_L')
    sensors =  db.relationship('Sensor', back_populates = 'tables_S')
    table_occup_data = db.relationship('Table_occupancy_data', back_populates = 'tables_O', cascade ='all', lazy=True, uselist=True)
    
    def __init__(self, table_id, location_id): 
        self.table_id = table_id
        self.location_id = location_id

    #json format
    def serialize(self): 
        return { 
            'table_id' : self.table_id,
            'location_id' : self.location_id
        }

class Table_occupancy_data(db.Model):
    __tablename__ = 'table_occupancy_data' #database table name, optionally specified 

    reading_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    occupied = db.Column(db.Boolean, unique=False, default=True)
    table_id = db.Column(db.String(50), db.ForeignKey('tables.table_id'), unique=False, nullable=False)

    #one-to-many model   
    tables_O = db.relationship('Tables', back_populates = 'table_occup_data')

    def __init__(self, timestamp, occupied, table_id): 
        self.timestamp = timestamp
        self.occupied = occupied
        self.table_id = table_id

    #json format
    def serialize(self): 
        return { 
            'timestamp' : self.timestamp,
            'table_id' : self.table_id,
            'occupied' : self.occupied
        }

class Env_sensor_data(db.Model):
    __tablename__ = 'env_sensor_data'

    reading_id = db.Column(db.Integer, primary_key=True) # does autoincrement
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    sensor_id = db.Column(db.String(100), nullable=False) #composite foreign key
    sensor_type = db.Column(db.String(30), nullable=False) #composite foreign key
    reading = db.Column(db.String(80), unique = False, nullable = False)

    __table_args__ = (db.ForeignKeyConstraint(['sensor_type', 'sensor_id'], ['sensor.sensor_type', 'sensor.sensor_id']), {})
    
    # one-to-many model
    sensor = db.relationship('Sensor', back_populates='env_sensor_readings')

    def __init__(self, timestamp, sensor_id, sensor_type, reading): 
        self.timestamp = timestamp 
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.reading = reading
    
    def serialize(self): 
        return { 
            'reading_id' : self.reading_id,
            'timestamp': self.timestamp, 
            'sensor_type': self.sensor_type, 
            'sensor_id': self.sensor_id, 
            'reading': self.reading 
        }

class Occupancy_sensor_data(db.Model):
    __tablename__ = 'occupancy_sensor_data'

    reading_id = db.Column(db.Integer, primary_key=True) # does autoincrement
    timestamp = db.Column(db.DateTime, unique=False, nullable=False)
    sensor_id = db.Column(db.String(100), nullable=False) #composite foreign key
    sensor_type = db.Column(db.String(30), nullable=False) #composite foreign key
    reading = db.Column(db.String(80), unique = False, nullable = False)

    __table_args__ = (db.ForeignKeyConstraint(['sensor_type', 'sensor_id'], ['sensor.sensor_type', 'sensor.sensor_id']), {})
    
    # one-to-many model
    sensor_1 = db.relationship('Sensor', back_populates='occupancy_sensor_readings')

    def __init__(self, timestamp, sensor_id, sensor_type, reading): 
        self.timestamp = timestamp 
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.reading = reading
    
    def serialize(self): 
        return { 
            'reading_id' : self.reading_id,
            'timestamp': self.timestamp, 
            'sensor_type': self.sensor_type, 
            'sensor_id': self.sensor_id, 
            'reading': self.reading 
        }