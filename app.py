from flask import Flask, render_template, Response, request
from camera_pi import Camera
import serial
import time




def getENVdata():
    arduino = serial.Serial('/dev/ttyACM0',9600)
 #   time.sleep(2)
    value1 = str(eval(arduino.readline()))
    value2 = str(eval(arduino.readline()))
    print (value1)
    print (value2)
    return value1, value2
    
app = Flask(__name__)

@app.route('/')
def index():
    if request.headers.get('accept') == 'text/event-stream':
        def events():
           # value1, value2 = getENVdata()
            while True:
                value1, value2 = getENVdata()
                yield "data: %s \s\s %s \n\n" % (value1, value2)
               # time.sleep(.1)
        return Response(events(), content_type='text/event-stream')
    return render_template('index.html')


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
    app.run(host='0.0.0.0', port =4003, debug=True, threaded=True)
