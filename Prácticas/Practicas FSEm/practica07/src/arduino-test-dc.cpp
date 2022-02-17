/*
* arduino-test-dc.cpp
*
* Author:  Mauricio Matamoros
* Date:    2020.03.01
* License: MIT
*
* Controls the power output of a resistive load using
* zero-cross detection and a TRIAC. Code for Arduino UNO
*
*/

// Digital 2 is Pin 2 in UNO
#define ZXPIN 2
// Digital 3 is Pin 3 in UNO
#define TRIAC 3

// Globals
volatile bool flag = false;
int step = 0;
int pfactor = 0;

// Prototypes
float read_temp(void);
float read_avg_temp(int count);

/**
* Setup the Arduino
*/
void setup(void){
	// Setup interupt pin (input)
	pinMode(ZXPIN, INPUT);
	attachInterrupt(digitalPinToInterrupt(ZXPIN), zxhandle, RISING);
	// Setup output (triac) pin
	pinMode(TRIAC, OUTPUT);
	// Blink led on interrupt
	pinMode(13, OUTPUT);

	// Setup the serial port to operate at 9600bps
	Serial.begin(9600);
}

void loop(){
	if(!flag){
		// Slack until next interrupt
		delay(1);
		return
	}
	// Reset flag & blink led
	flag = !flag;
	digitalWrite(13, LOW);
	// Enable power for STEP milliseconds
	if(pfactor < 8)
		digitalWrite(3, HIGH);
	delay(pfactor);
	// Disable power
	digitalWrite(3, LOW);
	// Increment/reset power factor every 20 cycles
	if(++step >= 19){
		step = 0;
		if(++pfactor > 8) pfactor = 0;
	}
}

void zxhandle(){
	flag = true;
	digitalWrite(13, HIGH);
}
