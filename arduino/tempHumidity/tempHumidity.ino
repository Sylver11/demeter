#include <dht.h> //importing temp sensor library
#include <LiquidCrystal.h> // importing LCD library

#define dataPin 7 // Defines pin number to which the sensor is connected
dht DHT; // Creats a DHT object
int pinOut = 6; // defines pin for relay
LiquidCrystal lcd(13, 12, 5, 4, 3, 2); // defines pins for LCD display

void setup() {
  Serial.begin(9600);
  pinMode(6, OUTPUT); // instruction on how to handle pin 6 (relay)
  lcd.begin(20, 4); // defines the size of the display columns * rows
}
void loop() {
  int readData = DHT.read22(dataPin); // Reads the data from the sensor
  float t = DHT.temperature; // Gets the values of the temperature
  float h = DHT.humidity; // Gets the values of the humidity
  lcd.setCursor(0,0);
  lcd.print("Temp: ");lcd.print(t); lcd.print(" "); lcd.print((char)223); lcd.print("C");
  lcd.setCursor(0, 1);
   lcd.print("Hum: ");lcd.print(h); lcd.print(" "); lcd.print("%");
  lcd.setCursor(0, 2);
  lcd.print("Soil: ");
  lcd.setCursor(0, 3);
  lcd.print("AirPr: ");
  // Printing the results on the serial monitor
//  Serial.print("Temperature = ");
//  Serial.print(t);
//  Serial.print(" *C ");
//  Serial.print("    Humidity = ");
//  Serial.print(h);
//  Serial.println(" % ");
  if (t >= 29){
    digitalWrite(pinOut, LOW);
  }
  else {
    digitalWrite(pinOut, HIGH);
  }
  
  delay(4000); // Delays 2 secods, as the DHT22 sampling rate is 0.5Hz
}
