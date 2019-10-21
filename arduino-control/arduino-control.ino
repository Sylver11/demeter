#include <Adafruit_BME280.h> //importing Temp/Hum/Pre library
#include <LiquidCrystal.h>


Adafruit_BME280 bme;
int pinOut1 = 8;
int pinOut2 = 9;
int pinOut3 = 10;
int pinOut4 = 11;

int maxTemp ;
int minTemp ;
int incoming[1];
int serialRead ; 

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
 while (!Serial) {
	; // wait for serial port to connect.
  }
}

void loop()
{

  for (int i = 0; i <= 100; i++)
  {
    sensorValue = sensorValue + analogRead(SensorPin);
    delay(1);
  }
  sensorValue = sensorValue / 100.0;

  Serial.println(bme.readTemperature());
  Serial.println(bme.readHumidity());
  Serial.println(sensorValue);

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
  lcd.print(maxTemp);



//if(Serial.available() > 0){      // if data present, blink
  //     digitalWrite(pinOut1, LOW);
    //   delay(1000);            
      // digitalWrite(pinOut1, HIGH);
      // delay(1000);
     //  Serial.flush();
// }

// serial read section
  while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
  {
    delay(30);  //delay to allow buffer to fill 
    if (Serial.available() >0)
    {
      maxTemp = Serial.read();  //gets one byte from serial buffer
     // readString = c; //makes the string readString
    }
  }

//  if (Serial.available() >= 0)
 // {
   //     int maxTemp = Serial.parseInt();
     //   int minTemp = Serial.parseInt();
  //  for (int i = 0; i < 1; i++)
   // {
    //  serialRead = Serial.read();
     // if (serialRead != -1) {
       // incoming[i] = serialRead;
    	// }
//	incoming[] =1,3
  // }

    if (bme.readTemperature() >= maxTemp)
    {
      digitalWrite(pinOut1, LOW);
   }
    else if (bme.readTemperature() <= minTemp)
    {
      digitalWrite(pinOut1, HIGH);
    }
  

  //  if (bme.readTemperature() >=30){
  //    digitalWrite(pinOut1, LOW);
  //  }
  //  else if (bme.readTemperature() <=27){
  //    digitalWrite(pinOut1, HIGH);
  //  }
  //////////////////////////////////////////////////////
  // while(Serial.available() >= 3){
  //    // fill array
  //    for (int i = 0; i < 3; i++){
  //      incoming[i] = Serial.read();
  //    }
  //    // instead of servo's we need to put the variables here from the if else statment above subsituting values 27 and 30 with variables
  //    servo0.write(incoming[0]);
  //    servo1.write(incoming[1]);
  //    servo2.write(incoming[2]);
  //  }
  ///////////////////////////////////////////////////

  delay(2000);
}
