/*
	ADXL345 Digital Accelerometer Wrapper
	
	Copyright 2010 Jan Anlauff <code at 23t.de>
	Adapted from Viliam Klein's Example (c) 2009
*/
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

#include "adxl345.h"
	
void adxl345_init(void) {
	uint8_t byte;
	
	// set slave select line to an output
	ADXL345_PORT_REGISTER |= _BV(ADXL345_SS);

	//long delay
	delay_ms(40);
	
	//waits for power register to respond correctly
	while(byte != 0x28) {
		// 0x28 is 0x00101000
		adxl345_set_register(POWER_CTL,0x28);
		_delay_us(5);
		byte = adxl345_get_register(POWER_CTL);
		printf("Power is: %x\n", byte);
	}

	delay_ms(1);

	// enable full-res output format
	adxl345_set_register(DATA_FORMAT,0x08);
	_delay_us(5);
	byte = adxl345_get_register(DATA_FORMAT);
	printf("Format is: %x\n", byte);
	
	adxl345_set_register(FIFO_CTL,0x00);
	_delay_us(5);
	byte = adxl345_get_register(FIFO_CTL);
	printf("FIFO is: %x\n", byte);
}

void adxl345_disable(void) {
	ADXL345_PORT |= _BV(ADXL345_SS);
}

void adxl345_enable(void) {
	ADXL345_PORT &= ~_BV(ADXL345_SS);
}
uint8_t adxl345_get_register(uint8_t register_name) {
	uint8_t ret;
	adxl345_enable();
	spi_transfer_wait(register_name | READ_MASK);
	ret =  spi_transfer_wait(ADXL345_NOP);
	adxl345_disable();
	return ret;
}

void adxl345_set_register(uint8_t register_name, uint8_t value) {
	adxl345_enable();
	spi_transfer_wait(register_name);
	spi_transfer_wait(value);
	adxl345_disable();
}

void adxl345_sample(uint16_t* values) {
		adxl345_enable();
		// 0x72 = 0b11110010, thus
		// Read-Mode
		// Multiple-Byte-Mode
		// leaves 110010, 0x32, DATAX0
		spi_transfer_wait(0xF2);
		
		for(uint8_t i=0; i<3; i++) {
			// assemble 16 signed int value
			adxl345_value.bytes[0] = (uint8_t)spi_transfer_wait(ADXL345_NOP);
			adxl345_value.bytes[1] = (uint8_t)spi_transfer_wait(ADXL345_NOP);
			values[i] =	adxl345_value.integer;
		}
	
		adxl345_disable();
}
