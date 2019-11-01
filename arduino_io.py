"""All io with the arduino
"""

from flask import session
import serial
import time


def _arduino_connection():
    arduino = serial.Serial(
        '/dev/ttyACM0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2,
        xonxoff=0,
        rtscts=0
        )
    arduino.setRTS(False)
    time.sleep(3)
    arduino.flush()
    return arduino



def write_temperature_settings(min_temperature, max_temperature):
   # session['channel_busy'] = True
    print(type(min_temperature))
   # min_temperature = str(min_temperature)
   # max_temperature = str(max_temperature)
    print(type(min_temperature))
    arduino = _arduino_connection()
    print("writing env settings from database to arduino")
    arduino.write(bytes('<', 'utf-8'))
    arduino.write(str(min_temperature).encode())
    arduino.write(str(max_temperature).encode())
    arduino.write(bytes('>', 'utf-8'))

   # session['channel_busy'] = False


def get_environment_data_from_arduino():

    arduino = _arduino_connection()
    data_str = arduino.read(arduino.inWaiting()).decode('ascii')
    return data_str
