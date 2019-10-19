/////////////// How to use the arduino-cli //////////////////////

Create new sketch:
arduino-cli sketch new arduino-control

To compile:
arduino-cli compile --fqbn arduino:avr:uno arduino-control.ino

Then change name of compiled from:
mv arduino-control.ino.arduino.avr.uno.hex arduino-control.arduino.avr.uno.hex

To upload use following command:
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno

Add library:
arduino-cli lib search "library you are looking for"

For more info go to: 
https://github.com/arduino/arduino-cli

/////////////////////////////////////////////////////////////
