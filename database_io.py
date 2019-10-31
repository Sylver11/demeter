from db_utils import db_connect
from datetime import datetime









ENVIRONMENT_SETTINGS_TABLE = 'env_settings'

def read_temperature_settings():
    con = db_connect()

    cursor = con.cursor()

    query = f"SELECT * FROM {ENVIRONMENT_SETTINGS_TABLE}"
    cursor.execute(query)

    _, min_temperature, max_temperature = cursor.fetchone()

    return min_temperature, max_temperature

def write_temperature_settings_to_database(a,b):
    con = db_connect()
    cur = con.cursor()
   # env_settings = """
   # CREATE TABLE env_settings (
   # ID INTEGER PRIMARY KEY AUTOINCREMENT,
   # min_temp INT,
   # max_temp INT,
   # datetime TEXT )"""
   # cur.execute(env_settings)
    time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    print(time)
    query = (
        f"INSERT INTO env_settings (min_temp, max_temp, datetime)"
        f"values ({int(a.decode('utf-8'))}, {int(b.decode('utf-8'))}, {time})")
    cur.execute(query)
    con.commit()
    print("temps settings have been written to the database")
