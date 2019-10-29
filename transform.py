"""All communication with io
goes through here.
"""

import database_io
import arduino_io



def update_temperature_settings():
    min_temperature, max_temperature = database_io.read_temperature_settings() 

    arduino_io.write_temperature_settings(min_temperature, max_temperature)
    
