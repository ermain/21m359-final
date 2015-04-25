#define MAX_FINGER_VAL 570 // We expect a max of 3.0 V at R = 7000
#define MIN_FINGER_VAL 250 // We expect a min of 1.0 V
#define FINGER_VAL_RANGE (MAX_FINGER_VAL - MIN_FINGER_VAL)
#define DATA_FIELDS 8

// data pin (SIG/COM on mux)
int data_pin = A0;
// address lines (S0-S3 on mux)
int mux_addr[4] = {10,11,12,13};

// data values
int data[DATA_FIELDS] = {0, 0, 0, 0, 0, 0, 0, 0};


void setup() {
  // initialize mux address lines
  for(int i = 0; i < 4; i++) {
    pinMode(mux_addr[i], OUTPUT);
    digitalWrite(mux_addr[i], LOW);
  }
  // initialize serial:
  Serial.begin(9600);

}

void change_addr(int addr) {
  for(int i = 0; i < 4; i++) {
    if((addr >> i) & 0x0001 == 1) {
      digitalWrite(mux_addr[i], HIGH);
    }
    else {
      digitalWrite(mux_addr[i], LOW);
    }
  }
}

// collect and transmit data.
void loop() {
  for(int i = 0; i < DATA_FIELDS; i++) {
    change_addr(i);
    delayMicroseconds(1);
    int data = analogRead(data_pin);
    Serial.print(data);
    Serial.print(" ");
  }
  Serial.println();
  //let's not innundate poor python :c
  //readline in python is called ~16.6 ms
  delay(17);
}

