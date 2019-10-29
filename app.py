from flask import Flask, render_template, Response, request, session
from camera_pi import Camera
import serial
import time
import re
from time import sleep
#from db_utils import db_connect

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

#def arduinoConn():
#    arduino = serial.Serial('/dev/ttyACM0',
#            baudrate=9600,
#            bytesize=serial.EIGHTBITS,
#            parity=serial.PARITY_NONE,
#            stopbits=serial.STOPBITS_ONE,
#            timeout=2,
#            xonxoff=0,
#            rtscts=0)
#    arduino.setRTS(False)
#    sleep(3)
#    arduino.flush()
#    arduin.setRTS(True)
#    return arduino

def getENVdata():
    if not session.get('channel_busy'):
       # arduino = arduinoConn()
      #  print(arduino.inWaiting())
       # data_str = arduino.read(arduino.inWaiting()).decode('ascii')
        data_str = arduino_io.get_environment_data_from_arduino()
        print(data_str)
        x = re.search("LockP", data_str)
      #  print(x)
        if re.search("LockP", data_str) is not None:
            print("LockP was received")
            session['channel_busy'] = True

            transform.update_temperature_settings()
           # transform.send_temperature_settings()
            value1 = "12"
            value2 = "12"
            value3 = "12"
            session['channel_busy'] = False
            return ("na",)*3
        #elif (arduino.inWaiting()>19):
        elif isinstance(data_str, tuple) and len(data_str) == 3:
           # print(arduino.inWaiting())
           # data_str = arduino.read(arduino.inWaiting()).decode('ascii')
            print("reading temps")
            data_str = [str(item) for item in data_str.split()]
            print(data_str)
            value1 = data_str[0]
            value2 = data_str[1]
            value3 = data_str[2]
            return value1, value2, value3
        else: 
            return ("ne",)*3
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
    a = bytes(request.args.get('temp', 0, type=str), 'utf-8')
    b = bytes(request.args.get('hum', 0, type=str), 'utf-8')
    database.io.write_temperature_settings_to_database(a, b)
   # with con:
   #     cur = con.cursor()
    #    cur.execute("INSERT INTO env_settings (id, temperature, humidity) values (?, ?, ?)",(1, a, b))
    #    con.commit()
    #    print("temps have been written to the database")
  #  return ''

# def arduinoWrite():
#     session['channel_busy'] = True
#    # print (session.get('channel_busy'))
#     print("arduino Write has been called")
#     arduino = arduinoConn()
#     with con:
#         cur = con.cursor()
#         cur.execute("SELECT * FROM env_settings")
#         a = "12"
#         _, b, c = cur.fetchone()
# 
#         print(f"b: {b}")
#         print(f"c: {c}")
# 
#         print("it successfully fetched the data from the database")
#         return a, b, c
#     print (a)
#     print (b)
#     arduino.write(bytes('<', 'utf-8'))
#     arduino.write(a)
#     arduino.write(b)
#     arduino.write(bytes('>', 'utf-8'))
#     session['channel_busy']= False
#     print (session.get('channel_busy'))
#     return "","",""


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
