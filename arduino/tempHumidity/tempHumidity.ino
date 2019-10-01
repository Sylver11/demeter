#include <Adafruit_BME280.h> //importing Temp/Hum/Pre library
#include <LiquidCrystal.h> // importing LCD library

//#define dataPin 8 // Defines pin number to which the sensor is connected
Adafruit_BME280 bme;
int pinOut1 = 9; // defines pin for relay
//int pinOut2 = 9; 
//int pinOut3 = 10; 
//int pinOut4 = 11; 

int incoming[1];//creating empty array for pyseries to populate values into it 

LiquidCrystal lcd(7, 6, 5, 4, 3, 2); // defines pins for LCD display

void setup() {
  Serial.begin(9600);
  pinMode(9, OUTPUT);
//  pinMode(9, OUTPUT);
//  pinMode(10, OUTPUT);
//  pinMode(11, OUTPUT);// instruction on how to handle pin 6 (relay)
  lcd.begin(20, 4); // defines the size of the display columns * rows

  if (!bme.begin())
  { 
    Serial.println("Error! No BMP Sensor Detected!!!");
    while (1);
  }
}
void loop() {
  int temp = bme.readTemperature();
  lcd.setCursor(0,0);
  lcd.print("Temp: ");lcd.print(bme.readTemperature()); lcd.print(" "); lcd.print((char)223); lcd.print("C");
  lcd.setCursor(0, 1);
  lcd.print("Hum: ");lcd.print(bme.readHumidity()); lcd.print(" "); lcd.print("%");
  lcd.setCursor(0, 2);
  lcd.print("Soil: ");
  lcd.setCursor(0, 3);
  lcd.print("AirPr: ");lcd.print(bme.readPressure() / 100); lcd.print(" mb");

  if (bme.readTemperature() >=30){
    digitalWrite(pinOut1, LOW);
  }
  else if (bme.readTemperature() <=27){
    digitalWrite(pinOut1, HIGH);
  }
//////////////////////////////////////////////////////
 while(Serial.available() >= 3){
    // fill array
    for (int i = 0; i < 3; i++){
      incoming[i] = Serial.read();
    }
    // instead of servo's we need to put the variables here from the if else statment above subsituting values 27 and 30 with variables
    servo0.write(incoming[0]);
    servo1.write(incoming[1]);
    servo2.write(incoming[2]);
  }
///////////////////////////////////////////////////


  
  delay(4000); // Delays 2 secods, as the DHT22 sampling rate is 0.5Hz
}
