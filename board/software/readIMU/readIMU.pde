// Copyright 2010 Jan Anlauff <code at 23t.de>
// This file is part of the Soldering Skaters Nokia Push Project
// (short: the project).
// 
// The project is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// The project is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with the project.  If not, see <http://www.gnu.org/licenses/>.

/*
	vim:ft=c
	Read all 6 Analog Inputs from Arduino Pro Mini
*/

int sensorValue = 0;
const int maxAnalogInPin = 5;
const int resetPin = 10;
int analogInPin = 0;
const char pinNames[6] = {'x','y','z','X','Y','Z'};
char serialCommand;
int channelToShow;
int mappedValue;

void setup() {
	pinMode(resetPin, OUTPUT);
	digitalWrite(resetPin, HIGH);
	delay(10);
	digitalWrite(resetPin, LOW);
	delay(2000);
	Serial.begin(115200);
}

void loop() {
	for(analogInPin = 0; analogInPin <= maxAnalogInPin; analogInPin++) {
		sensorValue = analogRead(analogInPin);
		Serial.print(pinNames[analogInPin]);
		Serial.print(sensorValue);
	}
	Serial.println();
	// wait 10 milliseconds before the next loop
	// for the analog-to-digital converter to settle
	// after the last reading:
	delay(10);
}
