from flask import Flask, render_template, Response, request, session
from camera_pi import Camera
import serial
import time
import re
from time import sleep
from datetime import datetime
import struct

import transform
import arduino_io
import database_io


app = Flask(__name__)


def getENVdata():
    data_str = arduino_io.get_environment_data_from_arduino()
    print(len(data_str))
    if re.search("LockP", data_str) is not None:
        print("LockP was received")
        transform.update_env_settings()
        return ("none",)*3
    elif len(data_str) >= 18 and len(data_str) <= 23:
        print("reading temps")
        data_str = [str(item) for item in data_str.split()]
        print(data_str)
        value1 = data_str[0]
        value2 = data_str[1]
        value3 = data_str[2]
        return value1, value2, value3
    else: 
        return ("none",)*3

@app.route('/_scheduled_Update')
def scheduled_Update():
    getENVdata()
    return ''

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lights/')
def lights():
    # start, stop= transform.display_light_settings_views()
    min_temperature, max_temperature, start, stop = transform.update_env_settings()
    # start = struct.unpack('<H',start)
    env_settings = {
        'start': int(start),
        'stop': int(stop),
        'min_temperature':int(min_temperature),
        'max_temperature':int(max_temperature)
    }
    return render_template('lights.html', env_settings=env_settings)


@app.route('/temperature/')
def temperature():
    return render_template('temperature.html')


@app.route('/feed')
def ENVdata():
    if request.headers.get('accept') == 'text/event-stream':
        value1, value2, value3 = getENVdata()
        return Response("data: %s %s %s \n\n" % (value1, value2, value3), content_type='text/event-stream')

# @app.route('/_display-light')
# def display_light_settings():
#     start, stop = transform.display_light_settings_views()
#     return Response(start, stop)

@app.route('/_temp')
def add_numbers():
    a = bytes(request.args.get('temp', 0, type=str), 'utf-8')
    b = bytes(request.args.get('hum', 0, type=str), 'utf-8')
    database_io.write_temperature_settings_to_database(a, b)
    return Response()

@app.route('/_light')
def set_light_time():
    #capture start stop time and write to the database. 
    a = bytes(request.args.get('start', 0, type=str), 'utf-8')
    b = bytes(request.args.get('stop', 0, type=str), 'utf-8')
    print(a)
    print(b)
    database_io.write_light_settings_to_database(a,b)
    return Response()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
