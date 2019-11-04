from db_utils import db_connect
from datetime import datetime

ENVIRONMENT_SETTINGS_TABLE = 'env_settings'

def read_temperature_settings():
    con = db_connect()
    cursor = con.cursor()
    query = f"SELECT * FROM {ENVIRONMENT_SETTINGS_TABLE} WHERE ID = (SELECT Max(ID) FROM {ENVIRONMENT_SETTINGS_TABLE})"
    cursor.execute(query)
    _, min_temperature, max_temperature, _ = cursor.fetchone()
    return min_temperature, max_temperature

def read_light_settings():
    con = db_connect()
    cursor = con.cursor()
    query = f"SELECT * FROM light_settings WHERE ID = (SELECT Max(ID) FROM light_settings)"
    cursor.execute(query)
    _, start, stop, _ = cursor.fetchone()
    return start, stop

def write_temperature_settings_to_database(a,b):
    con = db_connect()
    cur = con.cursor()
    a = int(a.decode('utf-8'))
    b = int(b.decode('utf-8'))
   # env_settings = """
   # CREATE TABLE env_settings (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # min_temp INT,
   # max_temp INT,
   # datetime TEXT )"""
   # cur.execute(env_settings)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print(type(time))
    print(type(a))
    query = "INSERT INTO env_settings (min_temp, max_temp, datetime) VALUES (?,?,?);"
    cur.execute(query, (a, b, time))
    con.commit()
    print("temps settings have been written to the database")

def write_light_settings_to_database(a,b):
    con = db_connect()
    cur = con.cursor()     
   # light_settings = """
   # CREATE TABLE light_settings (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # start CHAR(60),
   # stop CHAR(60),
   # datetime TEXT )"""
   # cur.execute(light_settings)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print(type(a))
    query = "INSERT INTO light_settings (start, stop, datetime) VALUES (?,?,?);"
    cur.execute(query, (a, b, time))
    con.commit()
    print("light settings have been written to the database")

