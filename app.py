from flask import Flask, render_template, Response, request, session
from camera_pi import Camera
import serial
import time
from time import sleep

def arduinoConn():
    arduino = serial.Serial('/dev/ttyACM0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,
            xonxoff=0,
            rtscts=0)
    arduino.setRTS(False)
    sleep(3)
    arduino.flush()
    arduino.setRTS(True)
    return arduino

def getENVdata():
    if (session.get('channel_busy')==False):
        arduino = arduinoConn()
        if (arduino.inWaiting()>19):
            print(arduino.inWaiting())
            data_str = arduino.read(arduino.inWaiting()).decode('ascii')
            data_str = [str(item) for item in data_str.split()]
            print(data_str)
            value1 = data_str[0]
            value2 = data_str[1]
            value3 = data_str[2]
            return value1, value2, value3
        else:
            return '','',''
    else:
        return '','',''
    
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
    session['channel_busy'] = True
    print (session.get('channel_busy'))
    arduino = arduinoConn()
    print (a)
    print (b)
    arduino.write(bytes('<', 'utf-8'))
    arduino.write(a)
    arduino.write(b)
    arduino.write(bytes('>', 'utf-8'))
    session['channel_busy']= False
    print (session.get('channel_busy'))
    return ""


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
