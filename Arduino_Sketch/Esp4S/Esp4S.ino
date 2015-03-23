/*
  Esplora For Scratch/Snap!
 
Copyright (c) 2013-15 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU  General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


 This sketch is largely based upon the EsploraRemote sketch 
 supplied as part of the Arduino Esplora Library within the Arduino IDE.
 */

#include <Esplora.h>
#define TINKERKIT_OUT_A 3
#define TINKERKIT_OUT_B 11
#define LED_PIN 13
#define dumpLoopTime 30  // 30 milliseconds
#define version "1.00"

/* timer variables */
unsigned long currentMillis;        // store the current value from millis()
unsigned long previousMillis;       // for comparison with currentMillis
int samplingInterval = 25;          // how often to run the main loop (in ms)

boolean continuousDump = false;

void setup() {
  while (!Serial); // needed for Leonardo-based board like Esplora
  Serial.begin(57600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(TINKERKIT_OUT_A, OUTPUT);
  pinMode(TINKERKIT_OUT_B, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    parseCommand();
  }
  if(continuousDump == true) {
    currentMillis = millis();
    if (currentMillis - previousMillis > samplingInterval) {
      previousMillis += samplingInterval;
      dumpInputs();
    }
  }
}

/*
 * This function reads a character from the serial line and
 * decide what to do next. The "what to do" part is given by
 * function it calls (e.g. dumpInputs(), setRed() and so on).
 */
void parseCommand() {
  char cmd = Serial.read();
  switch (cmd) {
    case 'D':
      dumpInputs(); // this is a one shot
      break;
    case 'C':
      dumpContinuos();
      break;
    case 'S':
      stopContinuous();
      break;
    case 'V':
      getVersion();
      break;
    case 'R':
      setRed();
      break;
    case 'G':
      setGreen();
      break;
    case 'B':
      setBlue();
      break;
    case 'T':
      setTone();
      break;
    case 'L':
      setLed13();
      break ;
    case 'Y':
      setTinkerKit1();
      break;
    case 'Z':
      setTinkerKit2();
      break;
  }
}

void dumpInputs() {
  Serial.print("ESP,");
  Serial.print(Esplora.readButton(SWITCH_1));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_2));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_3));
  Serial.print(',');
  Serial.print(Esplora.readButton(SWITCH_4));
  Serial.print(',');
  Serial.print(Esplora.readSlider());
  Serial.print(',');
  Serial.print(Esplora.readLightSensor());
  Serial.print(',');
  Serial.print(Esplora.readTemperature(DEGREES_C));
  Serial.print(',');
  Serial.print(Esplora.readMicrophone());
  Serial.print(',');
  Serial.print(Esplora.readJoystickSwitch());
  Serial.print(',');
  Serial.print(Esplora.readJoystickX());
  Serial.print(',');
  Serial.print(Esplora.readJoystickY());
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(X_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(Y_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readAccelerometer(Z_AXIS));
  Serial.print(',');
  Serial.print(Esplora.readTinkerkitInputA());
  Serial.print(',');
  Serial.print(Esplora.readTinkerkitInputB());
  Serial.print(',');
  Serial.print("PSE");
  Serial.println();
  
}

void setRed() {
  Esplora.writeRed(Serial.parseInt());
}

void setGreen() {
  Esplora.writeGreen(Serial.parseInt());
}

void setBlue() {
  Esplora.writeBlue(Serial.parseInt());
}

void setTone() {
  Esplora.tone(Serial.parseInt());
}

void setLed13() {
  int ledState = Serial.parseInt();
  if( ledState != 0 )
  {
     ledState = 1;
  }
  digitalWrite(LED_PIN, ledState);
}

void setTinkerKit1() {
  analogWrite(TINKERKIT_OUT_A, Serial.parseInt());
}

void setTinkerKit2() {
  analogWrite(TINKERKIT_OUT_B, Serial.parseInt());
}

void getVersion() {
  Serial.println(version);
}

void dumpContinuos() {
  continuousDump = true;
}

void stopContinuous() {
  continuousDump = false;
}

 
  
