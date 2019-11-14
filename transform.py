"""All communication with io
goes through here.
"""

import database_io
import arduino_io

def update_env_settings():
    min_temperature, max_temperature = database_io.read_temperature_settings() 
    start, stop = database_io.read_light_settings()
    arduino_io.write_env_settings(start, stop, min_temperature, max_temperature)
    return min_temperature, max_temperature, start, stop 

def display_light_settings_views():
    start, stop = database_io.read_light_settings()
    return start, stop



