"""All io with the arduino

"""
from flask import session
import serial
import time
from datetime import datetime

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

def write_env_settings(start, stop, min_temperature, max_temperature):
    arduino = _arduino_connection()
    now = datetime.now()
    current_time = now.strftime("%H")
    print("writing temperature and light settings from database to arduino")
    arduino.write(bytes('<', 'utf-8'))
    if (int(current_time) > int(start.decode('ascii')) and int(current_time) < int(stop.decode('ascii'))):
        arduino.write(bytes('L', 'utf-8'))
        arduino.write(bytes('1', 'utf-8'))
        print("lights are being switched on")
    else:
        arduino.write(bytes('L', 'utf-8'))
        arduino.write(bytes('0', 'utf-8'))
        print("lights are being turned off")
    arduino.write(str(min_temperature).encode())
    arduino.write(str(max_temperature).encode())
    arduino.write(bytes('>', 'utf-8'))

def get_environment_data_from_arduino():
    arduino = _arduino_connection()
    data_str = arduino.read(arduino.inWaiting()).decode('ascii')
    return data_str
