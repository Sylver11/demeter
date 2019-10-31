from flask import Flask, render_template, Response, request, session
from camera_pi import Camera
import serial
import time
import re
from time import sleep
from datetime import datetime

import transform
import arduino_io
import database_io

#con = db_connect() # connect to the database
#cur = con.cursor() # instantiate a cursor obj
#lock_sql = """
#CREATE TABLE lock (
#id integer PRIMARY KEY,
#busy BOOLEAN NOT NULL CHECK (busy IN (0,1)))"""
#cur.execute(lock_sql)


#env_settings = """
#CREATE TABLE env_settings (
#id integer,
#temperature TEXT,
#humidity TEXT )"""

#cur.execute(env_settings)


#when receiving the string lockP the lock tables must be set to 1 and changed to 0 again after it has written to the arduino
#when writing to the arduino it needs to grab the lastest set of values written to the env_settings table


def getENVdata():
    if not session.get('channel_busy'):
        data_str = arduino_io.get_environment_data_from_arduino()
        print(len(data_str))
       # x = re.search("LockP", data_str)
        if re.search("LockP", data_str) is not None:
            print("LockP was received")
            session['channel_busy'] = True
            transform.update_temperature_settings()
            session['channel_busy'] = False
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
    else:
        return 'none','none','none'
    
app = Flask(__name__)

@app.route('/')
def index():
    channel_busy = {'key':'value'}
    session['channel_busy'] = False
    return render_template('index.html')

@app.route('/feed')
def ENVdata():
    if request.headers.get('accept') == 'text/event-stream':
        value1, value2, value3 = getENVdata()
        return Response("data: %s %s %s \n\n" % (value1, value2, value3), content_type='text/event-stream')


@app.route('/_temp')
def add_numbers():
    now = datetime.now()
    print("now =", now)
    a = bytes(request.args.get('temp', 0, type=str), 'utf-8')
    b = bytes(request.args.get('hum', 0, type=str), 'utf-8')
    c = now.strftime("%d/%m/%Y %H:%M:%S")
    database_io.write_temperature_settings_to_database(a, b)
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
