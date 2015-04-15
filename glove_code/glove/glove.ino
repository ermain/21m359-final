#include <SevSeg.h>

#define MAX_FINGER_VAL 570 // We expect a max of 3.0 V at R = 7000
#define MIN_FINGER_VAL 250 // We expect a min of 1.0 V
#define FINGER_VAL_RANGE (MAX_FINGER_VAL - MIN_FINGER_VAL)

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
//Create an instance of the object.
SevSeg myDisplay;

// Finger values
int finger_1 = 0;
int finger_2 = 0;
int finger_3 = 0;
int finger_4 = 0;
int finger_1_pin = A0;
int finger_2_pin = A1;
int finger_3_pin = A2;
int finger_4_pin = A3;

void setup() {
  // put your setup code here, to run once:
// initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  
  int displayType = COMMON_CATHODE; //Your display is either common cathode or common anode

  //This pinout is for a bubble display
  //Declare what pins are connected to the GND pins (cathodes)
  int digit1 = 8; //Pin 1
  int digit2 = 5; //Pin 10
  int digit3 = 11; //Pin 4
  int digit4 = 13; //Pin 6

  //Declare what pins are connected to the segments (anodes)
  int segA = 7; //Pin 12
  int segB = 6; //Pin 11
  int segC = 10; //Pin 3
  int segD = 3; //Pin 8
  int segE = 9; //Pin 2
  int segF = 4; //Pin 9
  int segG = 2; //Pin 7
  int segDP= 12; //Pin 5
 
  int numberOfDigits = 4; //Do you have a 1, 2 or 4 digit display?

  myDisplay.Begin(displayType, numberOfDigits, digit1, digit2, digit3, digit4, segA, segB, segC, segD, segE, segF, segG, segDP);
  
  myDisplay.SetBrightness(100); //Set the display to 100% brightness level
}

void loop() {
  char transmit_string[100]; 
  char tempString[5];
  finger_1 = analogRead(finger_1_pin);
  finger_2 = analogRead(finger_2_pin);
  finger_3 = analogRead(finger_3_pin);
  finger_4 = analogRead(finger_4_pin);
  finger_1 = constrain(finger_1, MIN_FINGER_VAL, MAX_FINGER_VAL);
  finger_2 = constrain(finger_2, MIN_FINGER_VAL, MAX_FINGER_VAL);
  finger_3 = constrain(finger_3, MIN_FINGER_VAL, MAX_FINGER_VAL);
  finger_4 = constrain(finger_4, MIN_FINGER_VAL, MAX_FINGER_VAL);
  float fing_1 = (float)(finger_1 - MIN_FINGER_VAL)/FINGER_VAL_RANGE;
  float fing_2 = (float)(finger_2 - MIN_FINGER_VAL)/FINGER_VAL_RANGE;
  float fing_3 = (float)(finger_3 - MIN_FINGER_VAL)/FINGER_VAL_RANGE;
  float fing_4 = (float)(finger_4 - MIN_FINGER_VAL)/FINGER_VAL_RANGE;
  tempString[0] = (char)(fing_4 * 9) + '0';
  tempString[1] = (char)(fing_3 * 9) + '0';
  tempString[2] = (char)(fing_2 * 9) + '0';
  tempString[3] = (char)(fing_1 * 9) + '0';
  tempString[4] = '\0';
  //Produce an output on the display
  myDisplay.DisplayString(tempString, 0); //(numberToDisplay, decimal point location)

  //Transmit data over Bluetooth.
  sprintf(transmit_string, "%d %d %d %d", finger_1, finger_2, finger_3, finger_4);
  Serial.println(transmit_string);
  //let's not innundate poor python :c
  //readline in python is called ~16.6 ms
  delay(17);
}

