from db_utils import db_connect


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
    cur = execute("INSERT INTO env_settings (id, temperature, humidity) values (?, ?, ?",(1, a, b))
    con.commit()
    print("temps settings have been written to the database")
