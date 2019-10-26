#include <Adafruit_BME280.h> //importing Temp/Hum/Pre library
#include <LiquidCrystal.h>


Adafruit_BME280 bme;
int pinOut1 = 8;
int pinOut2 = 9;
int pinOut3 = 10;
int pinOut4 = 11;

int maxTemp ;
int minTemp ;
int lock = false; 

const byte numChars = 6;
char receivedChars[numChars];
//int receivedChars = 0;
boolean newData = false;
static boolean recvInProgress = false;


#define SensorPin A0
float sensorValue = 0;
String readString;
LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);

 digitalWrite(pinOut1, HIGH);  
 digitalWrite(pinOut2, HIGH);  
 digitalWrite(pinOut3, HIGH);  
 digitalWrite(pinOut4, HIGH);  
 
  lcd.begin(20, 4);

  if (!bme.begin())
  {
    Serial.println("Error! No BMP Sensor Detected!!!");
    while (1);
  }
// while (!Serial) {
//	; // wait for serial port to connect.
//  }
}

void loop()
{
  for (int i = 0; i <= 100; i++)
  {
    sensorValue = sensorValue + analogRead(SensorPin);
    delay(1);
  }
  sensorValue = sensorValue / 100.0;

  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(bme.readTemperature());
  lcd.print(" ");
  lcd.print((char)223);
  lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Hum: ");
  lcd.print(bme.readHumidity());
  lcd.print(" ");
  lcd.print("%");
  lcd.setCursor(0, 2);
  lcd.print("Soil: ");
  lcd.print(sensorValue);
  lcd.setCursor(0, 3);
  //lcd.print("AirPr: ");lcd.print(bme.readPressure() / 100); lcd.print(" mb");
  lcd.print(receivedChars[0]);lcd.print(receivedChars[1]);lcd.print("high is:");lcd.print(receivedChars[2]);lcd.print(receivedChars[3]);



    if (bme.readTemperature() >= maxTemp)
    {
      digitalWrite(pinOut1, LOW);
   }
    else if (bme.readTemperature() <= minTemp)
    {
      digitalWrite(pinOut1, HIGH);
    }
  

 showNewData();

  delay(5000);
}

//print serial every 5 sec with hum and temp. At the second round print lockN and wait  5 additonal second to receive data. thereafter it prints to serial again 
//script contiunelay checks what lock variable is set to and when lock is set to 1 then write variable from stored value to arduino and set lock again to 0   
//python receives lockN and sets lock to 1 and 


void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && lock == true) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {;
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
               // newData = true;
		lock = false;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
	else {
	    lock = false;
	}
    }
}

void showNewData() {
  //   while (!Serial) {
//	; // wait for serial port to connect.
//	}
    if (lock == false){
	Serial.println(bme.readTemperature());
        Serial.println(bme.readHumidity());
        Serial.println(sensorValue);
	lock = true;
	}
    else if (lock == true){
	Serial.println("LockP");
	recvWithStartEndMarkers(); 
	}

   // if (newData == true) {
//	Serial.println(bme.readTemperature());    
//	Serial.println(bme.readHumidity());
//	Serial.println(sensorValue);
//	newData = false;
//    }
}
